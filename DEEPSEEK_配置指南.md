# DeepSeek 配置指南

## ✅ 问题已修复

已修复 DeepSeek 不支持 Streamlit Cloud Secrets 的问题。现在 DeepSeek 完全支持从 Streamlit Secrets 读取 API 密钥！

---

## ⚡ 快速配置（3步完成）

### 步骤 1: 获取 DeepSeek API 密钥

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册并登录
3. 创建 API Key
4. 复制 API Key（格式：`sk-...`）

### 步骤 2: 在 Streamlit Cloud 配置 Secrets

访问您的 Streamlit Cloud 应用：
1. 点击 **Settings** → **Secrets**
2. 粘贴以下配置：

```toml
[llm]
DEEPSEEK_API_KEY = "sk-your-actual-deepseek-api-key"
```

3. 点击 **Save** 保存

### 步骤 3: 在应用中选择 DeepSeek

1. 等待应用重启（10-30秒）
2. 刷新应用页面
3. 侧边栏 → **LLM提供商** → 选择 **🚀 DeepSeek V3**
4. 选择模型：
   - **DeepSeek Chat** - 💬 通用对话模型
   - **DeepSeek Reasoner** - 🧠 推理模型
5. 开始分析！

---

## 🔧 修复详情

### 修复前的问题

```
❌ 分析失败: 使用DeepSeek需要设置DEEPSEEK_API_KEY环境变量
```

**原因**：DeepSeek 的初始化代码只从环境变量读取，不支持 Streamlit Secrets。

### 修复后的代码

**文件**: `tradingagents/graph/trading_graph.py`

```python
# 修复前（只支持环境变量）
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')  # ❌ 不支持 Secrets

# 修复后（支持 Streamlit Secrets）
try:
    from tradingagents.utils.secrets_helper import get_deepseek_api_key
    deepseek_api_key = get_deepseek_api_key() or os.getenv('DEEPSEEK_API_KEY')
except ImportError:
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

if not deepseek_api_key:
    raise ValueError(
        "DEEPSEEK_API_KEY 环境变量未设置。\n"
        "请在 Streamlit Cloud 的 Secrets 中配置，或在 .env 文件中设置。"
    )
```

---

## 📋 DeepSeek 双模型介绍

### 1. DeepSeek Chat (deepseek-chat)
- 💬 **类型**：通用对话模型
- ⚡ **特点**：响应快速，成本经济
- 🎯 **适用场景**：
  - 日常股票分析
  - 快速查询
  - 简单任务
  - 研究深度 1-2 级

### 2. DeepSeek Reasoner (deepseek-reasoner)
- 🧠 **类型**：推理模型
- 💡 **特点**：深度思考，推理能力强
- 🎯 **适用场景**：
  - 复杂分析
  - 深度推理
  - 多因素综合分析
  - 研究深度 3-5 级

---

## 💰 DeepSeek 定价优势

DeepSeek 以**性价比高**著称：

| 模型 | 输入成本 | 输出成本 | 适用场景 |
|------|---------|---------|---------|
| DeepSeek Chat | 低 | 低 | 日常分析 |
| DeepSeek Reasoner | 中 | 中 | 深度分析 |

相比 OpenAI GPT-4，DeepSeek 的成本显著更低，但性能接近！

---

## 🌐 DeepSeek 网络要求

- ✅ **国内可直接访问**
- ✅ 无需科学上网
- ✅ API 响应速度快
- ✅ 稳定可靠

---

## 📝 完整配置示例

### 最小配置（仅 DeepSeek）

```toml
[llm]
DEEPSEEK_API_KEY = "sk-your-actual-deepseek-api-key"
```

### 推荐配置（DeepSeek + 备用）

```toml
[llm]
# DeepSeek（主要使用，性价比高）
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key"

# OpenAI（备用）
OPENAI_API_KEY = "sk-your-openai-api-key"
```

---

## 🎯 使用建议

### 场景 1: 成本敏感型
**推荐配置**：
- LLM 提供商：DeepSeek
- 模型：DeepSeek Chat
- 研究深度：1-2 级

**优势**：成本最低，速度快

### 场景 2: 质量优先型
**推荐配置**：
- LLM 提供商：DeepSeek
- 模型：DeepSeek Reasoner
- 研究深度：4-5 级

**优势**：分析质量高，成本仍然合理

### 场景 3: 平衡型
**推荐配置**：
- LLM 提供商：DeepSeek
- 模型：根据任务选择 Chat 或 Reasoner
- 研究深度：3 级

**优势**：性能和成本平衡

---

## 🔍 验证配置

配置成功后，侧边栏的 **🔑 API密钥状态** 应显示：

```
可选配置:
✅ DeepSeek: sk-xxx...
```

---

## 🆘 故障排除

### 问题 1: "DEEPSEEK_API_KEY 环境变量未设置"

**解决方案**：
1. 检查 Streamlit Cloud Secrets 中是否配置了 `DEEPSEEK_API_KEY`
2. 确保格式正确（在 `[llm]` 节下）
3. 保存后等待应用重启
4. 刷新浏览器

### 问题 2: API Key 格式错误

**检查清单**：
- ✅ 以 `sk-` 开头
- ✅ 长度足够（通常 40+ 字符）
- ✅ 没有多余的空格或引号
- ✅ 在 DeepSeek 平台确认密钥有效

### 问题 3: API 调用失败

**解决方案**：
1. 检查 API Key 是否有效
2. 检查 DeepSeek 账户余额
3. 查看应用日志获取详细错误信息
4. 确认网络连接正常

---

## 📊 提交历史

```
1189bb8 fix: add Streamlit Secrets support for DeepSeek API key
ea7e6a3 feat: add DeepSeek dual model support (deepseek-chat and deepseek-reasoner)
```

**修复内容**：
- ✅ 添加 Streamlit Secrets 支持
- ✅ 改进错误提示信息
- ✅ 支持双模型选择
- ✅ 完全兼容 Streamlit Cloud

---

## ✨ 总结

DeepSeek 现在：
- ✅ **完全支持 Streamlit Cloud Secrets**
- ✅ **提供两个模型选择**（Chat 和 Reasoner）
- ✅ **性价比极高**
- ✅ **国内可直接访问**
- ✅ **配置简单快速**

只需配置 `DEEPSEEK_API_KEY`，即可开始使用！🎉

---

## 🔗 相关链接

- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [DeepSeek 定价](https://platform.deepseek.com/pricing)

---

**更新日期**: 2025-10-06  
**状态**: ✅ 已完成并部署

