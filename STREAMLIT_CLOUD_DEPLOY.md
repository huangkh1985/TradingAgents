# Streamlit Cloud 部署指南

## 📱 通过 Streamlit Cloud 实现移动端运行

本指南将帮助你将 TradingAgents-CN 项目部署到 Streamlit Cloud，实现通过移动端访问。

---

## 🚀 部署前准备

### 1. GitHub 仓库准备

确保你的项目已经上传到 GitHub，并且：
- ✅ 代码已推送到 GitHub
- ✅ 仓库设置为 Public（公开）或 Private（需要授权）
- ✅ 主分支包含最新代码

### 2. 必需文件检查

确保项目根目录包含以下文件：

#### ✅ 已有文件
- `web/app.py` - Streamlit 应用主入口
- `pyproject.toml` - Python 依赖配置
- `.streamlit/config.toml` - Streamlit 配置

#### 📝 需要创建的文件
- `.streamlit/secrets.toml` - 环境变量配置（仅本地，不要上传）
- `packages.txt` - 系统级依赖（如果需要）
- `streamlit_app.py` - Cloud 部署入口

---

## 📦 步骤 1: 创建云部署入口文件

在项目根目录创建 `streamlit_app.py`（Streamlit Cloud 默认入口）：

```python
#!/usr/bin/env python3
"""
Streamlit Cloud 部署入口
自动重定向到 web/app.py
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入并运行 web 应用
if __name__ == "__main__":
    import runpy
    runpy.run_path("web/app.py", run_name="__main__")
```

---

## 🔐 步骤 2: 配置环境变量

### 方式 A: 通过 Streamlit Cloud 界面配置（推荐）

1. 登录 [Streamlit Cloud](https://share.streamlit.io/)
2. 部署应用后，进入应用设置
3. 点击 **Settings** → **Secrets**
4. 添加以下配置（根据实际需求）：

```toml
# LLM API 配置
OPENAI_API_KEY = "your-openai-api-key"
DASHSCOPE_API_KEY = "your-dashscope-api-key"
GOOGLE_API_KEY = "your-google-api-key"

# 数据源 API 配置
TUSHARE_TOKEN = "your-tushare-token"
REDDIT_CLIENT_ID = "your-reddit-client-id"
REDDIT_CLIENT_SECRET = "your-reddit-client-secret"
FINNHUB_API_KEY = "your-finnhub-api-key"

# 数据库配置（如果使用）
MONGODB_URI = "your-mongodb-uri"
REDIS_URL = "your-redis-url"

# 应用配置
DEFAULT_MODEL_PROVIDER = "openai"
DEFAULT_MODEL_NAME = "gpt-4"
```

### 方式 B: 本地创建示例文件

创建 `.streamlit/secrets.toml.example`（作为模板）：

```toml
# 这是环境变量配置模板
# 复制此文件为 secrets.toml 并填入真实值
# 注意：不要将 secrets.toml 上传到 GitHub

[api_keys]
OPENAI_API_KEY = ""
DASHSCOPE_API_KEY = ""
GOOGLE_API_KEY = ""

[data_sources]
TUSHARE_TOKEN = ""
REDDIT_CLIENT_ID = ""
REDDIT_CLIENT_SECRET = ""
FINNHUB_API_KEY = ""

[database]
MONGODB_URI = ""
REDIS_URL = ""
```

---

## 🛠️ 步骤 3: 调整依赖配置

### 选项 A: 使用简化的 requirements.txt（推荐云部署）

在根目录更新 `requirements.txt`，移除不必要的依赖：

```txt
# 核心依赖
streamlit>=1.28.0
plotly>=5.0.0
pandas>=2.0.0
python-dotenv>=1.0.0

# LLM 相关
openai>=1.0.0,<2.0.0
langchain-openai>=0.1.0
langchain-google-genai>=2.1.0
google-generativeai>=0.8.0
langgraph>=0.4.0

# 数据源
yfinance>=0.2.0
akshare>=1.14.0
tushare>=1.4.0
finnhub-python>=2.4.0

# 工具库
requests>=2.31.0
feedparser>=6.0.0
markdown>=3.4.0
pytz>=2024.0
```

### 选项 B: 使用 pyproject.toml

如果使用 `pyproject.toml`，Streamlit Cloud 会自动识别并安装依赖。

---

## 🔧 步骤 4: 调整 Streamlit 配置

更新 `.streamlit/config.toml` 适配云环境：

```toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[logger]
level = "info"

[theme]
base = "light"
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
showErrorDetails = false  # 生产环境隐藏错误详情
```

---

## 🌐 步骤 5: 在 Streamlit Cloud 上部署

### 5.1 登录 Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io/)
2. 使用 GitHub 账号登录

### 5.2 创建新应用

1. 点击 **"New app"** 按钮
2. 选择你的 GitHub 仓库
3. 配置部署信息：
   - **Repository**: `你的用户名/TradingAgents-CN`
   - **Branch**: `main` 或 `master`
   - **Main file path**: `streamlit_app.py`（或 `web/app.py`）

### 5.3 高级设置（可选）

点击 **"Advanced settings"**：
- **Python version**: 选择 `3.10` 或更高
- **Secrets**: 粘贴环境变量配置
- **Resources**: 根据需要选择资源配置

### 5.4 部署应用

1. 点击 **"Deploy!"** 开始部署
2. 等待 3-10 分钟，Streamlit Cloud 将：
   - 克隆你的仓库
   - 安装依赖
   - 启动应用

3. 部署完成后，你会获得一个公开 URL：
   ```
   https://你的应用名.streamlit.app
   ```

---

## 📱 步骤 6: 移动端访问

### 6.1 直接访问

1. 在手机浏览器输入你的应用 URL
2. 应用会自动适配移动端界面

### 6.2 添加到主屏幕（PWA 体验）

#### iOS (iPhone/iPad)
1. 在 Safari 浏览器打开应用
2. 点击底部分享按钮
3. 选择"添加到主屏幕"
4. 输入应用名称，点击"添加"

#### Android
1. 在 Chrome 浏览器打开应用
2. 点击右上角菜单
3. 选择"添加到主屏幕"
4. 确认添加

### 6.3 优化移动端体验

在 `web/app.py` 中添加移动端适配代码：

```python
# 检测移动设备
import streamlit as st

def is_mobile():
    """检测是否为移动设备"""
    try:
        # 通过 JavaScript 检测
        is_mobile = st.runtime.get_client_device_type() == "mobile"
        return is_mobile
    except:
        return False

# 根据设备调整布局
if is_mobile():
    st.set_page_config(
        layout="centered",  # 移动端使用居中布局
        initial_sidebar_state="collapsed"  # 默认收起侧边栏
    )
else:
    st.set_page_config(
        layout="wide",  # 桌面端使用宽屏布局
        initial_sidebar_state="expanded"
    )
```

---

## 🔍 步骤 7: 监控和维护

### 7.1 查看日志

1. 登录 Streamlit Cloud
2. 进入你的应用管理页面
3. 点击 **"Manage app"** → **"Logs"**
4. 查看实时运行日志和错误信息

### 7.2 更新应用

应用会自动更新！当你推送新代码到 GitHub 时：
- Streamlit Cloud 会自动检测
- 重新部署应用（约 2-5 分钟）

### 7.3 重启应用

如果应用出现问题：
1. 进入应用管理页面
2. 点击 **"Reboot app"**
3. 应用会在 30 秒内重启

---

## ⚠️ 常见问题和注意事项

### 1. 资源限制

**免费版 Streamlit Cloud 限制：**
- CPU: 1 核心
- 内存: 1GB
- 存储: 有限
- 运行时间: 空闲一段时间后休眠

**解决方案：**
- 优化代码，减少内存使用
- 使用缓存机制 (`@st.cache_data`, `@st.cache_resource`)
- 升级到付费版获得更多资源

### 2. 数据库连接

如果使用 MongoDB/Redis：
- 使用云数据库服务（MongoDB Atlas, Redis Cloud）
- 在 Secrets 中配置连接字符串
- 确保数据库允许外部连接

### 3. API 密钥安全

- ⚠️ **永远不要**将 API 密钥直接写在代码中
- ✅ 使用 Streamlit Secrets 管理敏感信息
- ✅ 将 `.streamlit/secrets.toml` 添加到 `.gitignore`

### 4. 文件上传和存储

- Streamlit Cloud 不持久化文件存储
- 上传的文件在应用重启后会丢失
- 需要持久化存储请使用云存储服务（AWS S3, Cloudinary 等）

### 5. 应用性能优化

```python
# 使用缓存优化性能
@st.cache_data(ttl=3600)  # 缓存 1 小时
def load_stock_data(symbol):
    """加载股票数据"""
    return fetch_data(symbol)

@st.cache_resource
def init_llm_client():
    """初始化 LLM 客户端（只初始化一次）"""
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
```

### 6. 移动端布局问题

如果移动端显示异常：
- 检查是否使用了固定宽度的容器
- 使用 Streamlit 的响应式布局组件
- 测试不同屏幕尺寸的显示效果

---

## 📚 附加资源

### 官方文档
- [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit 部署指南](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [管理 Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

### 最佳实践
- [Streamlit 性能优化](https://docs.streamlit.io/library/advanced-features/caching)
- [应用安全指南](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/app-authentication)

---

## ✅ 部署检查清单

在部署前，请确认：

- [ ] 代码已推送到 GitHub
- [ ] 创建了 `streamlit_app.py` 入口文件
- [ ] `.streamlit/config.toml` 已配置
- [ ] `requirements.txt` 或 `pyproject.toml` 包含所有依赖
- [ ] 敏感信息已从代码中移除
- [ ] API 密钥已在 Streamlit Secrets 中配置
- [ ] 本地测试运行正常
- [ ] `.gitignore` 包含 `secrets.toml`
- [ ] 数据库连接（如有）已配置云服务
- [ ] 应用在移动端浏览器测试通过

---

## 🎉 完成部署！

部署完成后，你将获得：
- 🌐 可在任何设备访问的 Web 应用
- 📱 移动端友好的界面
- 🔄 自动更新机制
- 📊 实时监控和日志
- 🚀 无需服务器维护

**现在你可以在手机、平板、电脑上随时访问你的交易分析系统了！**

---

## 🆘 需要帮助？

如有问题，请：
1. 查看 [Streamlit Community](https://discuss.streamlit.io/)
2. 检查应用日志
3. 提交 [GitHub Issue](https://github.com/你的用户名/TradingAgents-CN/issues)

