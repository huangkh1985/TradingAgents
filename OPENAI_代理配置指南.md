# OpenAI 代理配置指南（仅使用 OpenAI）

## 🎯 配置目标

仅使用 OpenAI（通过代理），不需要其他 LLM 提供商。

---

## ⚡ 快速配置（3步完成）

### 步骤 1: 获取 OpenAI API 密钥

1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 登录并创建 API Key
3. 复制 API Key（格式：`sk-...`）

### 步骤 2: 配置 Streamlit Cloud Secrets

访问您的 Streamlit Cloud 应用：
1. 点击 **Settings** → **Secrets**
2. 粘贴以下配置：

#### 方式 A: 使用 OpenAI 官方端点

```toml
[llm]
OPENAI_API_KEY = "sk-your-actual-openai-api-key"
```

#### 方式 B: 使用 OpenAI 代理端点（推荐）

```toml
[llm]
OPENAI_API_KEY = "sk-your-actual-openai-api-key"
OPENAI_API_BASE = "https://your-proxy-url.com/v1"  # 替换为您的代理地址
```

#### 常用代理端点示例

```toml
[llm]
OPENAI_API_KEY = "sk-your-actual-openai-api-key"

# 示例1: 使用 OpenAI 代理服务
OPENAI_API_BASE = "https://api.openai-proxy.com/v1"

# 示例2: 使用自建代理
# OPENAI_API_BASE = "https://your-domain.com/v1"

# 示例3: 使用其他中转服务
# OPENAI_API_BASE = "https://api.openai-sb.com/v1"
```

3. 点击 **Save** 保存

### 步骤 3: 在应用中选择 OpenAI

1. 等待应用重启（10-30秒）
2. 刷新应用页面
3. 侧边栏 → **LLM提供商** → 选择 **🤖 OpenAI**
4. 选择模型（推荐 GPT-4o 或 GPT-4o Mini）
5. 开始使用！

---

## 🔧 使用自定义 OpenAI 端点（灵活配置）

如果您的代理不完全兼容 OpenAI 格式，或者需要更灵活的配置：

### 配置 Secrets

```toml
[llm]
# 自定义 OpenAI 端点的密钥
CUSTOM_OPENAI_API_KEY = "your-api-key"
```

### 在应用中配置

1. 侧边栏 → **LLM提供商** → 选择 **🔧 自定义OpenAI端点**
2. 填写 **API端点URL**：`https://your-proxy-url.com/v1`
3. 填写 **API密钥**（或留空，如果在 Secrets 中配置了）
4. 选择模型或自定义模型名称
5. 开始使用！

---

## 📋 完整的最小配置

仅使用 OpenAI 的最小配置：

```toml
[llm]
# OpenAI API 配置
OPENAI_API_KEY = "sk-your-actual-openai-api-key"
OPENAI_API_BASE = "https://your-proxy-url.com/v1"  # 可选，使用代理时配置
```

**就这么简单！** 不需要配置任何其他 LLM 提供商。

---

## ✅ 验证配置

配置成功后，侧边栏的 **🔑 API密钥状态** 应显示：

```
✅ OpenAI: sk-xxx...
```

---

## 🚀 推荐的 OpenAI 模型

根据您的需求选择：

### 1. GPT-4o（推荐）
- **特点**：最新旗舰模型，性能最强
- **适合**：复杂分析、专业任务
- **选择**：侧边栏 → 选择 "GPT-4o - 最新旗舰模型"

### 2. GPT-4o Mini（经济推荐）
- **特点**：轻量旗舰，性价比高
- **适合**：日常分析、快速任务
- **选择**：侧边栏 → 选择 "GPT-4o Mini - 轻量旗舰"

### 3. GPT-4 Turbo
- **特点**：强化版本，稳定可靠
- **适合**：标准分析任务
- **选择**：侧边栏 → 选择 "GPT-4 Turbo - 强化版"

---

## 🔍 常见代理配置问题

### 问题 1: 代理端点格式错误

**错误配置**：
```toml
OPENAI_API_BASE = "https://your-proxy.com"  # ❌ 缺少 /v1
```

**正确配置**：
```toml
OPENAI_API_BASE = "https://your-proxy.com/v1"  # ✅ 包含 /v1
```

### 问题 2: API Key 格式错误

**检查清单**：
- ✅ 以 `sk-` 开头
- ✅ 长度足够（通常 40+ 字符）
- ✅ 没有多余的空格或引号

### 问题 3: 代理不工作

**排查步骤**：
1. 检查代理 URL 是否可访问
2. 确认 API Key 在代理服务中有效
3. 查看应用日志：Streamlit Cloud → Manage → Logs
4. 尝试使用 OpenAI 官方端点测试 API Key 是否有效

---

## 💡 提示

### 关于其他 LLM 提供商
- ✅ 应用支持多种 LLM 提供商，但您**不需要配置它们**
- ✅ 只需在侧边栏选择 **🤖 OpenAI** 即可
- ✅ 其他提供商的配置可以忽略

### 关于数据源
- ✅ **AKShare** 是默认数据源，**免费且无需配置**
- ✅ 应用会自动使用 AKShare 获取股票数据
- ✅ 无需配置 FinnHub、Tushare 等其他数据源

---

## 📝 配置示例

### 示例 1: 使用 OpenAI 官方（需要科学上网）

```toml
[llm]
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"
```

### 示例 2: 使用 OpenAI 代理（推荐）

```toml
[llm]
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://api.openai-proxy.com/v1"
```

### 示例 3: 使用自建代理

```toml
[llm]
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://my-openai-proxy.example.com/v1"
```

---

## 🆘 故障排除

### 错误: "OPENAI_API_KEY 环境变量未设置"

**解决方案**：
1. 检查 Streamlit Cloud Secrets 中是否配置了 `OPENAI_API_KEY`
2. 确保格式正确（在 `[llm]` 节下）
3. 保存后等待应用重启
4. 刷新浏览器

### 错误: "API 调用失败"

**解决方案**：
1. 检查 API Key 是否有效
2. 检查代理端点是否可访问
3. 检查 API Key 余额是否充足
4. 查看应用日志获取详细错误信息

### 错误: "连接超时"

**解决方案**：
1. 检查代理服务器是否正常
2. 尝试更换代理端点
3. 检查网络连接

---

## 📞 需要帮助？

如果遇到问题：

1. **查看应用日志**：
   - Streamlit Cloud → Your App → Manage → Logs

2. **检查配置格式**：
   - 确保 TOML 格式正确
   - 确保在 `[llm]` 节下

3. **测试 API Key**：
   - 在本地或其他工具中测试 API Key 是否有效

4. **提交问题**：
   - [GitHub Issues](https://github.com/huangkh1985/TradingAgents/issues)

---

## ✨ 总结

仅使用 OpenAI（代理）的配置非常简单：

1. ✅ 获取 OpenAI API Key
2. ✅ 在 Streamlit Cloud Secrets 配置：
   ```toml
   [llm]
   OPENAI_API_KEY = "sk-your-key"
   OPENAI_API_BASE = "https://your-proxy.com/v1"  # 可选
   ```
3. ✅ 侧边栏选择 "🤖 OpenAI"
4. ✅ 开始分析！

**就是这么简单！** 🎉

---

**更新日期**: 2025-10-06  
**适用版本**: v1.0.3+

