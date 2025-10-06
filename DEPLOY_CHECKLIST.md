# 🚀 Streamlit Cloud 快速部署清单

## 📋 部署前检查（5分钟完成）

### ✅ 第一步：检查文件

确保以下文件存在并正确配置：

- [x] `streamlit_app.py` - 云部署入口（已创建）
- [x] `.streamlit/config.toml` - Streamlit 配置（已更新）
- [x] `.streamlit/secrets.toml.example` - 环境变量示例（已创建）
- [x] `requirements.txt` 或 `pyproject.toml` - 依赖配置（已存在）
- [ ] `.gitignore` 包含 `secrets.toml`（需检查）

### ✅ 第二步：推送到 GitHub

```bash
# 添加新文件
git add streamlit_app.py .streamlit/secrets.toml.example .streamlit/config.toml STREAMLIT_CLOUD_DEPLOY.md

# 提交更改
git commit -m "准备 Streamlit Cloud 部署配置"

# 推送到 GitHub
git push origin main
```

### ✅ 第三步：登录 Streamlit Cloud

1. 访问: https://share.streamlit.io/
2. 使用 GitHub 账号登录
3. 授权 Streamlit Cloud 访问你的仓库

### ✅ 第四步：创建应用

1. 点击 **"New app"**
2. 选择配置：
   - **Repository**: `你的用户名/TradingAgents-CN`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. 点击 **"Advanced settings"**（可选）
4. 点击 **"Deploy!"**

### ✅ 第五步：配置环境变量

1. 等待应用部署完成
2. 进入应用设置: **Settings** → **Secrets**
3. 参考 `.streamlit/secrets.toml.example`，添加必要的 API 密钥：

```toml
# 最小配置（必需）
[llm]
OPENAI_API_KEY = "sk-your-openai-api-key"

# 或使用其他 LLM 服务商
DASHSCOPE_API_KEY = "your-dashscope-key"
GOOGLE_API_KEY = "your-google-key"

# 如果需要 A股数据
[data_sources]
TUSHARE_TOKEN = "your-tushare-token"
```

4. 保存后应用会自动重启

### ✅ 第六步：测试移动端访问

1. 获取应用 URL: `https://你的应用名.streamlit.app`
2. 在手机浏览器打开测试
3. 添加到手机主屏幕：
   - **iOS**: Safari → 分享 → 添加到主屏幕
   - **Android**: Chrome → 菜单 → 添加到主屏幕

---

## ⚡ 最小依赖部署（推荐）

如果完整依赖安装失败，可以使用最小依赖：

创建 `requirements.txt`（简化版）：

```txt
streamlit>=1.28.0
plotly>=5.0.0
pandas>=2.0.0
openai>=1.0.0
langchain-openai>=0.1.0
langgraph>=0.4.0
yfinance>=0.2.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## 🔧 常见问题快速修复

### 问题 1: 依赖安装超时

**解决方案**: 简化 requirements.txt，只保留核心依赖

### 问题 2: 应用启动失败

**检查**:
1. Streamlit Cloud 日志查看错误信息
2. 确认 `streamlit_app.py` 路径正确
3. 检查 Python 版本（需要 3.10+）

### 问题 3: API 密钥未生效

**解决方案**:
1. 确认 Secrets 格式正确（TOML 格式）
2. 保存后等待应用重启
3. 在代码中使用 `st.secrets["KEY_NAME"]` 访问

### 问题 4: 移动端布局错误

**优化代码**:
```python
# 在 web/app.py 顶部添加
import streamlit as st

st.set_page_config(
    page_title="TradingAgents",
    page_icon="📈",
    layout="centered",  # 移动端友好
    initial_sidebar_state="collapsed"  # 默认收起侧边栏
)
```

---

## 📱 移动端优化建议

### 1. 响应式布局

```python
# 检测设备类型
is_mobile = st.session_state.get('is_mobile', False)

# 调整列数
if is_mobile:
    col1 = st.container()  # 单列布局
else:
    col1, col2 = st.columns(2)  # 双列布局
```

### 2. 简化输入表单

- 使用 `st.selectbox` 替代复杂输入
- 提供预设选项
- 减少必填字段

### 3. 优化加载速度

```python
# 使用缓存
@st.cache_data(ttl=3600)
def load_data(symbol):
    return fetch_stock_data(symbol)

# 延迟加载非关键内容
with st.expander("高级选项"):
    # 高级配置放在折叠区域
    pass
```

---

## 🎯 部署成功标志

当你看到以下内容时，说明部署成功：

✅ Streamlit Cloud 状态显示 "Running"  
✅ 访问应用 URL 能看到界面  
✅ 移动端可以正常打开和操作  
✅ API 调用正常（能进行股票分析）  
✅ 日志没有严重错误  

---

## 📞 获取帮助

- **Streamlit 官方文档**: https://docs.streamlit.io/
- **Community 论坛**: https://discuss.streamlit.io/
- **项目 Issues**: https://github.com/你的用户名/TradingAgents-CN/issues

---

## 🎉 部署完成！

恭喜！你的 TradingAgents 应用现在可以：

- 🌐 在任何设备访问
- 📱 移动端友好使用
- 🔄 代码推送自动更新
- 🆓 免费托管（免费版）
- 🚀 无需服务器维护

**享受你的 AI 交易分析助手吧！**

