# DeepSeek API 配置修复说明

## 问题描述

在使用 DeepSeek 作为 LLM 时，出现 401 认证错误：
```
❌ 分析失败: Error code: 401 - {'error': {'message': 'Authentication Fails, Your api key: ****be08 is invalid', 'type': 'authentication_error', 'param': None, 'code': 'invalid_request_error'}}
```

## 问题根源

### 1. 代码问题（已修复）

在 `tradingagents/graph/trading_graph.py` 文件中，DeepSeek BASE_URL 的读取使用了 `os.getenv()`：

```python
# 旧代码 - 错误
deepseek_base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
```

在 **Streamlit Cloud 环境**下，`os.getenv()` **无法读取** Streamlit Secrets 中的配置。这导致即使在 Secrets 中配置了 `DEEPSEEK_BASE_URL`，程序仍然使用默认值。

### 2. 配置问题

用户在 Streamlit Secrets 中的配置：
```toml
[llm]
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"  # ❌ 错误！
```

**DeepSeek API 的正确 BASE_URL 不需要 `/v1` 后缀！**

## 修复方案

### 1. 代码修复（已完成）

修改 `tradingagents/graph/trading_graph.py` 使用 `secrets_helper` 正确读取配置：

```python
# 新代码 - 正确
try:
    from tradingagents.utils.secrets_helper import get_deepseek_api_key, get_api_base_url
    deepseek_api_key = get_deepseek_api_key() or os.getenv('DEEPSEEK_API_KEY')
    deepseek_base_url = get_api_base_url('deepseek') or os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
except ImportError:
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    deepseek_base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
```

### 2. 配置修复（需要用户操作）

#### Streamlit Cloud Secrets 正确配置：

```toml
[llm]
# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-96af8f5cea7...........5dbe08"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"  # ✅ 正确！不要加 /v1
```

**重要说明：**
- ✅ **正确**：`https://api.deepseek.com`
- ❌ **错误**：`https://api.deepseek.com/v1`
- ❌ **错误**：`https://api.deepseek.com/`

DeepSeek API 的 BASE_URL 与 OpenAI 不同，**不需要** `/v1` 后缀。

## DeepSeek API 端点说明

DeepSeek API 兼容 OpenAI 格式，但端点略有不同：

| 提供商 | BASE_URL | 完整端点 |
|--------|----------|---------|
| OpenAI | `https://api.openai.com/v1` | `https://api.openai.com/v1/chat/completions` |
| DeepSeek | `https://api.deepseek.com` | `https://api.deepseek.com/v1/chat/completions` |

注意：DeepSeek 的 BASE_URL 中**不包含** `/v1`，`/v1` 会在实际调用时由适配器自动添加。

## 验证 DeepSeek API 密钥

您可以使用以下方法验证 API 密钥是否有效：

### 方法1：使用 curl 测试

```bash
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-96af8f5cea7...........5dbe08" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": false
  }'
```

如果返回正常响应，说明 API 密钥有效。

### 方法2：在 Python 中测试

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-96af8f5cea7...........5dbe08",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)
```

## 完整的 Streamlit Cloud Secrets 配置示例

```toml
[llm]
# OpenAI（使用代理）
OPENAI_API_KEY = "sk-OQ6xiwqyiXYUpzNWe...........QSdJnQk"
OPENAI_API_BASE = "https://coultra.blueshirtmap.com/v1"

# DeepSeek（正确配置）
DEEPSEEK_API_KEY = "sk-96af8f5cea7...........5dbe08"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"  # ✅ 不要加 /v1

[data_sources]
# Finnhub
FINNHUB_API_KEY = "ctt5209r01qin3c1au......r01qin3c1auag"
```

## 部署步骤

1. **提交代码修复**：
   ```bash
   git add tradingagents/graph/trading_graph.py DEEPSEEK_API_CONFIG_FIX.md
   git commit -m "fix: 修复DeepSeek BASE_URL读取问题，支持从Streamlit Secrets正确读取配置"
   git push origin main
   ```

2. **更新 Streamlit Cloud Secrets**：
   - 登录 Streamlit Cloud
   - 进入应用设置
   - 编辑 Secrets
   - 修改 `DEEPSEEK_BASE_URL` 为 `https://api.deepseek.com`（移除 `/v1`）
   - 保存

3. **重启应用**（Streamlit Cloud 会自动重启）

4. **测试 DeepSeek 分析**

## 可能的其他问题

如果修复后仍然出现 401 错误，请检查：

### 1. API 密钥是否有效
- 登录 [DeepSeek 平台](https://platform.deepseek.com/)
- 检查 API 密钥状态
- 确认账户余额充足
- 必要时重新生成 API 密钥

### 2. API 密钥格式
- DeepSeek API 密钥应以 `sk-` 开头
- 长度通常为 48-64 个字符
- 不包含空格或特殊字符

### 3. 网络连接
- 确认 Streamlit Cloud 能够访问 `https://api.deepseek.com`
- 检查是否有防火墙或代理设置

### 4. 模型名称
确认使用的模型名称正确：
- ✅ `deepseek-chat`（通用对话模型）
- ✅ `deepseek-reasoner`（推理模型）
- ❌ `deepseek-v3`（不是有效的模型名称）

## 相关文件

- `tradingagents/graph/trading_graph.py` - DeepSeek LLM 初始化（已修复）
- `tradingagents/llm_adapters/deepseek_adapter.py` - DeepSeek 适配器
- `tradingagents/utils/secrets_helper.py` - Secrets 读取工具

## 总结

1. ✅ **代码问题已修复**：使用 `get_api_base_url()` 正确读取 Streamlit Secrets
2. ⚠️ **需要修改配置**：将 `DEEPSEEK_BASE_URL` 从 `https://api.deepseek.com/v1` 改为 `https://api.deepseek.com`
3. ✅ **验证 API 密钥**：确保 DeepSeek API 密钥有效且余额充足

修复后，DeepSeek 应该能够正常工作！🎉

