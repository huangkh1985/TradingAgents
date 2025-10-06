# Streamlit 配置说明

本目录包含 Streamlit 应用的配置文件。

## 📁 文件说明

### `config.toml`
Streamlit 应用的主配置文件，**针对 Streamlit Cloud 部署优化**。

**配置特点**：
- `headless = true` - 无头模式运行
- `enableCORS = true` - 启用跨域支持
- `enableXsrfProtection = true` - 安全保护
- 不指定固定的地址和端口

**使用场景**：
- ✅ Streamlit Cloud 部署（推荐）
- ✅ Docker 部署
- ⚠️ 本地开发（使用 `config.local.toml` 更方便）

### `config.local.toml`
本地开发专用配置文件（不会被提交到 Git）。

**配置特点**：
- `headless = false` - 自动打开浏览器
- `address = "localhost"` - 本地绑定
- `runOnSave = true` - 文件保存时自动重新运行
- `developmentMode = true` - 开发模式

**使用场景**：
- ✅ 本地开发（推荐）
- ❌ 云端部署（使用 `config.toml`）

### `secrets.toml` (需要创建)
存储敏感信息的配置文件，包括：
- API 密钥（OpenAI, DashScope, Google等）
- 数据库连接字符串
- 其他敏感配置

**⚠️ 安全提醒**：
- 此文件已添加到 `.gitignore`，不会被上传到 Git
- 请参考 `secrets.toml.example` 创建你自己的配置
- 永远不要将包含真实密钥的文件上传到公开仓库

### `secrets.toml.example`
`secrets.toml` 的模板文件，包含：
- 所有可配置项的说明
- 示例格式
- 使用指南

**使用方法**：
```bash
# 本地开发
cp secrets.toml.example secrets.toml
# 然后编辑 secrets.toml，填入真实的 API 密钥

# Streamlit Cloud 部署
# 不需要创建文件，直接在 Streamlit Cloud 界面配置
# Settings → Secrets → 复制 secrets.toml.example 的内容并填入真实密钥
```

## 🔧 配置优先级

Streamlit 按以下优先级读取配置：

1. 命令行参数（最高优先级）
2. 环境变量
3. `.streamlit/config.toml`
4. 全局配置 (`~/.streamlit/config.toml`)
5. 默认值（最低优先级）

Secrets 读取方式：
```python
import streamlit as st

# 读取 secrets.toml 中的配置
api_key = st.secrets["llm"]["OPENAI_API_KEY"]
```

## 📚 相关文档

- [Streamlit 配置文档](https://docs.streamlit.io/library/advanced-features/configuration)
- [Secrets 管理](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [主题定制](https://docs.streamlit.io/library/advanced-features/theming)

## 🎨 主题配置

当前主题使用浅色模式，你可以在 `config.toml` 中修改：

```toml
[theme]
base = "light"  # 或 "dark"
primaryColor = "#1f77b4"  # 主色调
backgroundColor = "#ffffff"  # 背景色
secondaryBackgroundColor = "#f0f2f6"  # 次要背景色
textColor = "#262730"  # 文字颜色
```

## 🚀 快速开始

### 本地开发
```bash
# 1. 创建 secrets 配置
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 2. 编辑并填入真实密钥
# 使用你喜欢的编辑器打开 .streamlit/secrets.toml

# 3. （可选）使用本地开发配置
# config.local.toml 已经存在，Streamlit 会优先使用它
# 如果不存在，会使用 config.toml（云端配置）

# 4. 运行应用
streamlit run streamlit_app.py
```

**配置文件选择逻辑**：
- 如果存在 `.streamlit/config.local.toml` → 使用本地配置
- 否则使用 `.streamlit/config.toml` → 使用云端配置

### Streamlit Cloud 部署
```bash
# 1. 确保使用云端兼容的 config.toml
# 已经配置好，无需修改

# 2. 推送代码到 GitHub
git add .streamlit/config.toml packages.txt
git commit -m "fix: Update Streamlit Cloud configuration"
git push origin main

# 3. Streamlit Cloud 自动检测更新并重新部署
# 等待几分钟，查看日志确认成功

# 4. 配置 Secrets（如果需要 API 功能）
# Settings → Secrets → 粘贴 secrets.toml.example 的内容并填入真实密钥
```

## ⚠️ 重要提示

### 本地开发 vs 云端部署

**本地开发时**：
- 使用 `config.local.toml`（已包含本地优化设置）
- 不会被提交到 Git（已在 `.gitignore` 中）
- 可以自动打开浏览器、热重载等

**云端部署时**：
- 使用 `config.toml`（已包含云端优化设置）
- 会被提交到 Git
- `config.local.toml` 不会影响云端部署

### 常见问题

**Q: 为什么需要两个配置文件？**

A: 本地开发和云端部署的环境不同：
- 本地：需要自动打开浏览器、热重载、localhost 绑定
- 云端：需要 headless 模式、CORS 支持、动态端口绑定

**Q: 我修改了 config.toml，会影响本地开发吗？**

A: 不会。如果存在 `config.local.toml`，Streamlit 会优先使用它。

**Q: 我要部署到云端，需要修改什么？**

A: 不需要修改配置文件，只需：
1. 推送代码到 GitHub
2. 在 Streamlit Cloud 的 Secrets 中配置 API 密钥
3. 等待部署完成

