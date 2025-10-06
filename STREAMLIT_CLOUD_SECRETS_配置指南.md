# Streamlit Cloud Secrets 配置指南

## 🔴 当前问题

您的应用运行失败，错误信息：
```
❌ 分析失败: DASHSCOPE_API_KEY 环境变量未设置
```

这是因为您选择了**阿里百炼（DashScope）**作为 LLM 提供商，但没有在 Streamlit Cloud 中配置相应的 API 密钥。

## 📝 解决方案

### 方案 1: 配置阿里百炼 API 密钥（推荐，如果您有该密钥）

#### 步骤 1: 获取 DashScope API 密钥

1. 访问 [阿里云百炼平台](https://dashscope.aliyun.com/)
2. 登录并进入控制台
3. 获取您的 API Key（格式类似：`sk-xxxxxxxxxxxxxx`）

#### 步骤 2: 在 Streamlit Cloud 配置 Secrets

1. 访问您的 Streamlit Cloud 应用管理页面
2. 点击右上角 **⚙️ Settings** → **Secrets**
3. 在 Secrets 编辑器中添加以下配置：

```toml
[llm]
DASHSCOPE_API_KEY = "sk-your-actual-dashscope-api-key"

[data_sources]
FINNHUB_API_KEY = "your-finnhub-api-key"  # 必需
```

4. 点击 **Save** 保存
5. 应用会自动重启

### 方案 2: 切换到其他 LLM 提供商（如果没有 DashScope 密钥）

如果您没有阿里百炼的 API 密钥，可以使用其他提供商：

#### 选项 A: 使用 OpenAI（推荐）

```toml
[llm]
OPENAI_API_KEY = "sk-your-openai-api-key"

[data_sources]
FINNHUB_API_KEY = "your-finnhub-api-key"  # 必需
```

然后在应用侧边栏中选择 **🤖 OpenAI** 作为 LLM 提供商。

#### 选项 B: 使用 Google Gemini（免费额度大）

```toml
[llm]
GOOGLE_API_KEY = "AIza-your-google-api-key"

[data_sources]
FINNHUB_API_KEY = "your-finnhub-api-key"  # 必需
```

获取 Google API Key：
1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 点击 "Get API key" 创建密钥
3. 复制密钥

然后在应用侧边栏中选择 **🌟 Google AI** 作为 LLM 提供商。

#### 选项 C: 使用 DeepSeek（中国友好，性价比高）

```toml
[llm]
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key"

[data_sources]
FINNHUB_API_KEY = "your-finnhub-api-key"  # 必需
```

获取 DeepSeek API Key：
1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册并获取 API Key

然后在应用侧边栏中选择 **🚀 DeepSeek V3** 作为 LLM 提供商。

## 📋 完整的 Secrets 配置模板

以下是一个推荐的完整配置（复制到 Streamlit Cloud Secrets）：

```toml
# =============================================================================
# LLM 服务商 API 配置（至少配置一个）
# =============================================================================

[llm]
# 选择您要使用的提供商，配置对应的 API Key

# OpenAI（如果使用）
OPENAI_API_KEY = "sk-your-openai-api-key"

# 阿里云百炼（如果使用）
DASHSCOPE_API_KEY = "sk-your-dashscope-api-key"

# Google Gemini（推荐，免费额度大）
GOOGLE_API_KEY = "AIza-your-google-api-key"

# DeepSeek（推荐，性价比高）
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key"

# 百度千帆（如果使用）
QIANFAN_AK = "your-qianfan-access-key"
QIANFAN_SK = "your-qianfan-secret-key"

# =============================================================================
# 金融数据源 API 配置（必需）
# =============================================================================

[data_sources]
# FinnHub（美股数据，必需配置）
FINNHUB_API_KEY = "your-finnhub-api-key"

# Tushare（A股数据，可选）
TUSHARE_TOKEN = "your-tushare-token"

# AKShare 无需配置，开箱即用
```

## 🔑 如何获取各个 API 密钥

### 必需配置

#### FinnHub API Key（美股数据，必需）
1. 访问 [FinnHub](https://finnhub.io/register)
2. 注册免费账户
3. 在 Dashboard 中获取 API Key

### LLM 提供商（至少配置一个）

#### Google Gemini（推荐：免费额度大，每天可免费调用）
1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用 Google 账号登录
3. 点击 "Create API Key"
4. 复制生成的 API Key（格式：`AIza...`）

#### OpenAI
1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 创建账户并充值（需要信用卡）
3. 创建 API Key

#### DeepSeek（推荐：中国友好）
1. 访问 [DeepSeek 平台](https://platform.deepseek.com/)
2. 注册并获取 API Key
3. 充值使用（价格实惠）

#### 阿里云百炼
1. 访问 [阿里云百炼](https://dashscope.aliyun.com/)
2. 阿里云账号登录
3. 开通服务并获取 API Key

### 可选配置

#### Tushare（A股专业数据）
1. 访问 [Tushare](https://tushare.pro/register)
2. 注册并获取 Token
3. 根据积分等级享受不同数据权限

## ⚠️ 重要提醒

1. **不要在代码中硬编码 API 密钥**
2. **不要将 secrets.toml 提交到 GitHub**
3. **定期检查 API 使用量，避免超额费用**
4. **至少配置一个 LLM 提供商的 API Key**
5. **FinnHub API Key 是必需的**（用于金融数据）

## 🚀 配置后的操作

1. 在 Streamlit Cloud Secrets 中保存配置
2. 等待应用自动重启（约 10-30 秒）
3. 刷新应用页面
4. 在侧边栏检查 API 密钥状态（应该显示 ✅）
5. 选择您配置的 LLM 提供商
6. 开始使用股票分析功能

## 🆘 故障排除

### 问题：保存 Secrets 后仍然提示未配置

**解决方案**：
1. 检查 TOML 格式是否正确（注意 `[llm]` 和 `[data_sources]` 节）
2. 确保没有多余的空格或引号错误
3. 强制重启应用：Settings → Reboot app
4. 清除浏览器缓存并刷新

### 问题：API Key 格式错误

**检查清单**：
- OpenAI: 应以 `sk-` 开头
- Google: 应以 `AIza` 开头
- DashScope: 应以 `sk-` 开头
- 确保复制完整的密钥，没有多余空格

### 问题：应用崩溃或无法启动

**解决方案**：
1. 检查 Secrets 的 TOML 格式
2. 查看应用日志（Manage app → Logs）
3. 确保至少配置了一个 LLM 提供商

## 📞 需要帮助？

如果遇到问题，请：
1. 检查应用日志：Streamlit Cloud → Your App → Manage → Logs
2. 查看本地是否能正常运行（使用 `.streamlit/secrets.toml`）
3. 在 [GitHub Issues](https://github.com/huangkh1985/TradingAgents/issues) 提问

---

**最后更新**: 2025-10-06

