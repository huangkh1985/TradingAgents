# 🐛 严重Bug修复：硬编码的 DashScope API 密钥检查

## 🔴 问题描述

**严重性**: 🔴 Critical（阻断性 Bug）

用户反馈：不管在侧边栏选择哪个 LLM 提供商（OpenAI、Google、DeepSeek 等），分析总是失败并提示：

```
❌ 分析失败: DASHSCOPE_API_KEY 环境变量未设置
```

## 🔍 问题根源

在 `web/utils/analysis_runner.py` 第 204-214 行，代码**硬编码**检查了 `DASHSCOPE_API_KEY`，完全忽略了用户选择的 LLM 提供商：

### 问题代码（修复前）

```python
# 验证环境变量
update_progress("检查环境变量配置...")
dashscope_key = os.getenv("DASHSCOPE_API_KEY")  # ❌ 硬编码检查 DashScope
finnhub_key = os.getenv("FINNHUB_API_KEY")

logger.info(f"环境变量检查:")
logger.info(f"  DASHSCOPE_API_KEY: {'已设置' if dashscope_key else '未设置'}")
logger.info(f"  FINNHUB_API_KEY: {'已设置' if finnhub_key else '未设置'}")

if not dashscope_key:  # ❌ 不管选择什么提供商，都检查 DashScope
    raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
if not finnhub_key:
    raise ValueError("FINNHUB_API_KEY 环境变量未设置")
```

### 问题分析

1. **硬编码检查**：代码始终检查 `DASHSCOPE_API_KEY`，不管用户选择了什么 LLM 提供商
2. **无视用户选择**：`llm_provider` 参数被完全忽略
3. **不支持 Streamlit Secrets**：使用 `os.getenv()` 无法读取 Streamlit Cloud 的 Secrets
4. **强制依赖 FinnHub**：要求必须配置 FinnHub，但实际上有 AKShare 作为免费替代

## ✅ 解决方案

### 修复后的代码

```python
# 验证环境变量 - 根据选择的 LLM 提供商动态检查
update_progress("检查环境变量配置...")

# 导入 secrets_helper 以支持 Streamlit Secrets
try:
    from tradingagents.utils.secrets_helper import get_api_key
except ImportError:
    # 回退到简单的环境变量读取
    def get_api_key(key_name, section=None):
        return os.getenv(key_name)

# 根据 llm_provider 检查对应的 API 密钥
llm_key_map = {
    "dashscope": ("DASHSCOPE_API_KEY", "llm"),
    "deepseek": ("DEEPSEEK_API_KEY", "llm"),
    "google": ("GOOGLE_API_KEY", "llm"),
    "openai": ("OPENAI_API_KEY", "llm"),
    "openrouter": ("OPENROUTER_API_KEY", "llm"),
    "siliconflow": ("SILICONFLOW_API_KEY", "llm"),
    "custom_openai": ("CUSTOM_OPENAI_API_KEY", "llm"),
    "qianfan": ("QIANFAN_AK", "llm"),
    "anthropic": ("ANTHROPIC_API_KEY", "llm"),
}

# 检查选择的 LLM 提供商的 API 密钥
if llm_provider.lower() in llm_key_map:
    key_name, section = llm_key_map[llm_provider.lower()]
    llm_api_key = get_api_key(key_name, section)
    
    logger.info(f"环境变量检查:")
    logger.info(f"  {key_name}: {'已设置' if llm_api_key else '未设置'}")
    
    if not llm_api_key:
        raise ValueError(
            f"{key_name} 环境变量未设置。\n"
            f"请在 Streamlit Cloud 的 Secrets 中配置，或在 .env 文件中设置。\n"
            f"当前选择的 LLM 提供商: {llm_provider}"
        )
else:
    logger.warning(f"⚠️ 未知的 LLM 提供商: {llm_provider}")

# FinnHub API 密钥是可选的（因为有 AKShare 作为备选）
finnhub_key = get_api_key("FINNHUB_API_KEY", "data_sources")
logger.info(f"  FINNHUB_API_KEY: {'已设置' if finnhub_key else '未设置（使用AKShare）'}")
```

### 改进要点

1. ✅ **动态检查**：根据 `llm_provider` 参数动态检查对应的 API 密钥
2. ✅ **支持所有提供商**：支持 dashscope、deepseek、google、openai、openrouter、siliconflow、qianfan、anthropic
3. ✅ **支持 Streamlit Secrets**：使用 `secrets_helper.get_api_key()` 读取配置
4. ✅ **更友好的错误信息**：明确告知用户缺少哪个 API 密钥以及如何配置
5. ✅ **FinnHub 可选**：FinnHub 不再强制要求（可使用 AKShare）

## 🔧 补充修复：扩展 secrets_helper.py

为了支持所有 LLM 提供商，在 `tradingagents/utils/secrets_helper.py` 中添加了以下函数：

```python
def get_openrouter_api_key() -> Optional[str]:
    """获取 OpenRouter API 密钥"""
    # OpenRouter 可以使用 OPENROUTER_API_KEY 或 OPENAI_API_KEY
    key = get_api_key("OPENROUTER_API_KEY", "llm")
    if not key:
        key = get_api_key("OPENAI_API_KEY", "llm")
    return key

def get_siliconflow_api_key() -> Optional[str]:
    """获取 SiliconFlow API 密钥"""
    return get_api_key("SILICONFLOW_API_KEY", "llm")

def get_qianfan_ak() -> Optional[str]:
    """获取 千帆 Access Key"""
    return get_api_key("QIANFAN_AK", "llm")

def get_qianfan_sk() -> Optional[str]:
    """获取 千帆 Secret Key"""
    return get_api_key("QIANFAN_SK", "llm")

def get_custom_openai_api_key() -> Optional[str]:
    """获取自定义 OpenAI API 密钥"""
    return get_api_key("CUSTOM_OPENAI_API_KEY", "llm")
```

## 📝 修改的文件

1. ✅ `web/utils/analysis_runner.py` - 修复硬编码的 API 密钥检查
2. ✅ `tradingagents/utils/secrets_helper.py` - 添加所有 LLM 提供商的密钥获取函数

## ✨ 预期效果

修复后：

1. ✅ 用户选择 **Google AI**，只检查 `GOOGLE_API_KEY`
2. ✅ 用户选择 **OpenAI**，只检查 `OPENAI_API_KEY`
3. ✅ 用户选择 **DeepSeek**，只检查 `DEEPSEEK_API_KEY`
4. ✅ 用户选择 **DashScope**，才检查 `DASHSCOPE_API_KEY`
5. ✅ 支持从 Streamlit Cloud Secrets 读取配置
6. ✅ 提供清晰的错误提示，告知用户如何配置

## 🧪 测试场景

### 场景 1: 使用 Google Gemini
- **配置**: 只在 Secrets 中设置 `GOOGLE_API_KEY`
- **选择**: 侧边栏选择 "🌟 Google AI"
- **结果**: ✅ 分析正常运行，不再要求 DASHSCOPE_API_KEY

### 场景 2: 使用 OpenAI
- **配置**: 只在 Secrets 中设置 `OPENAI_API_KEY`
- **选择**: 侧边栏选择 "🤖 OpenAI"
- **结果**: ✅ 分析正常运行，不再要求 DASHSCOPE_API_KEY

### 场景 3: 使用 DeepSeek
- **配置**: 只在 Secrets 中设置 `DEEPSEEK_API_KEY`
- **选择**: 侧边栏选择 "🚀 DeepSeek V3"
- **结果**: ✅ 分析正常运行，不再要求 DASHSCOPE_API_KEY

## 🎯 影响范围

- **受影响用户**: 所有不使用 DashScope 的用户
- **严重程度**: 🔴 Critical（完全阻止使用其他 LLM）
- **修复优先级**: 🔴 Highest（立即修复并部署）

## 📌 经验教训

1. ❌ **不要硬编码服务商依赖**：始终根据用户选择动态检查
2. ❌ **不要假设用户配置**：不要强制要求特定的 API 密钥
3. ✅ **支持多种配置方式**：同时支持环境变量和 Streamlit Secrets
4. ✅ **提供清晰的错误信息**：告诉用户缺少什么以及如何解决
5. ✅ **代码审查**：硬编码检查应该在代码审查中被发现

## 🚀 部署说明

此修复已准备好部署：

1. 提交到 Git
2. 推送到 GitHub
3. Streamlit Cloud 会自动重新部署
4. 用户无需更改任何配置，只需确保配置了选择的 LLM 提供商的 API 密钥

---

**修复日期**: 2025-10-06  
**状态**: ✅ 已完成  
**影响**: 🔴 Critical Bug Fix

