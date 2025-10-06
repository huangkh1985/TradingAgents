# Streamlit 配置说明

本目录包含 Streamlit 应用的配置文件。

## 📁 文件说明

### `config.toml`
Streamlit 应用的主配置文件，包括：
- 服务器配置（端口、地址、CORS等）
- 浏览器配置
- 主题设置（颜色、样式等）
- 客户端配置

**使用场景**：
- 本地开发
- Docker 部署
- Streamlit Cloud 部署

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

# 3. 运行应用
streamlit run streamlit_app.py
```

### Streamlit Cloud 部署
```bash
# 1. 推送代码到 GitHub
git push origin main

# 2. 在 Streamlit Cloud 创建应用
# 访问 https://share.streamlit.io/

# 3. 配置 Secrets
# Settings → Secrets → 粘贴 secrets.toml.example 的内容并填入真实密钥
```

