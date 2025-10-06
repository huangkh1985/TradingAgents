# 🔧 Streamlit Cloud Secrets 读取修复

**修复时间**: 2025-10-06  
**提交**: 834341e  
**状态**: ✅ 已推送，等待部署

---

## 🐛 问题

应用使用 `os.getenv()` 读取配置，但在 Streamlit Cloud 上必须使用 `st.secrets` 才能读取 Secrets 配置。

---

## ✅ 已修复

### 修改文件：
- `web/utils/api_checker.py` - 添加 `_get_secret()` 函数
- `web/components/sidebar.py` - 使用 `st.secrets` 读取密钥

### 核心修改：
```python
def _get_secret(key, section=None):
    """
    获取密钥，支持多种来源：
    1. Streamlit Secrets (优先，用于 Streamlit Cloud)
    2. 环境变量 (用于本地开发)
    """
    try:
        import streamlit as st
        if section:
            return st.secrets.get(section, {}).get(key)
        # ... fallback to os.getenv()
    except:
        return os.getenv(key)
```

---

## 📝 正确的 Secrets 配置

在 Streamlit Cloud 的 **Settings → Secrets** 中：

```toml
[llm]
OPENAI_API_KEY = "sk-your-actual-key"
OPENAI_API_BASE = "https://api.gptapi.us/v1/"
```

**注意**：
- ✅ 必须有 `[llm]` section 标题
- ✅ 使用双引号包裹值
- ✅ `=` 两边需要空格
- ❌ 不要用 `[app]` section

---

## 🚀 部署后效果

### 旧版本（错误）：
```
❌ DASHSCOPE_API_KEY: 未配置 (必需)
❌ FINNHUB_API_KEY: 未配置 (必需)
```

### 新版本（正确）：
```
✅ OpenAI API密钥: sk-SB9ajGFk... 
✅ AKShare: 已启用（免费）
```

---

**部署时间**: 预计 5-10 分钟  
**测试方法**: 强制刷新页面（Ctrl + Shift + R）


