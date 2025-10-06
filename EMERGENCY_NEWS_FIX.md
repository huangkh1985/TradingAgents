# 🚨 新闻获取紧急修复指南

## 问题：仍然无法获取新闻

### 🎯 最直接的解决方案（3分钟）

#### 步骤1：确认您的 Streamlit Secrets 配置

打开 Streamlit Cloud → 您的应用 → Settings → Secrets

**复制以下配置（已包含测试密钥）**：

```toml
# ===== 测试配置（立即可用）=====
[google_search]
API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
CX = "c09a7a52c4c364088"

# ===== LLM 配置（保留您自己的）=====
[llm]
OPENAI_API_KEY = "sk-OQ6xiwqyiXYUpzNWe...........QSdJnQk"
OPENAI_API_BASE = "https://coultra.blueshirtmap.com/v1"

DEEPSEEK_API_KEY = "sk-96af8f5cea7...........5dbe08"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ===== 数据源配置 =====
[data_sources]
FINNHUB_API_KEY = "ctt5209r01qin3c1au......r01qin3c1auag"
```

#### 步骤2：保存并重启

1. 点击"Save"保存配置
2. 应用会自动重启（等待30秒）
3. 刷新浏览器页面

#### 步骤3：验证

1. 在侧边栏找到 **"🔧 新闻调试工具"**（折叠框）
2. 展开后点击 **"🧪 测试 Google Custom Search API"**
3. 看到 "✅ API 正常！" 即表示成功

---

## 📋 如果还是看不到调试工具

### 方案A：手动验证配置

在浏览器中打开这个 URL：

```
https://www.googleapis.com/customsearch/v1?key=AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres&cx=c09a7a52c4c364088&q=002183+股票+新闻&num=3
```

**期望结果**：应该看到 JSON 数据，包含 `items` 数组和新闻标题。

**如果看到错误**：
- 403 错误 → API 未启用
- 429 错误 → 配额用完（使用自己的 API Key）
- 其他错误 → 配置有误

### 方案B：检查部署状态

1. **查看 Streamlit Cloud 部署日志**：
   - Streamlit Cloud → 您的应用 → Manage app → Logs
   - 搜索 `[Google Custom Search]`
   - 查看是否有错误信息

2. **确认最新代码已部署**：
   - 检查 GitHub 最新 commit：f1c71b7
   - 确认 Streamlit Cloud 显示的 commit 是最新的

### 方案C：强制重新部署

1. Streamlit Cloud → 您的应用 → Settings
2. 点击 "Reboot app"
3. 等待重启完成（1-2分钟）
4. 刷新浏览器

---

## 🔍 深度诊断

### 检查1：配置是否生效

在您的应用中添加临时代码（可以放在任何位置）：

```python
import streamlit as st

st.write("## 配置诊断")

if hasattr(st, 'secrets'):
    # 检查 google_search
    if 'google_search' in st.secrets:
        st.success("✅ 找到 [google_search] section")
        st.write(f"API_KEY: {st.secrets['google_search'].get('API_KEY', '未配置')[:20]}...")
        st.write(f"CX: {st.secrets['google_search'].get('CX', '未配置')[:15]}...")
    else:
        st.error("❌ [google_search] section 不存在")
else:
    st.error("❌ Streamlit Secrets 不可用")
```

### 检查2：测试 API 直接调用

```python
import streamlit as st
import requests

st.write("## API 测试")

api_key = st.secrets.get('google_search', {}).get('API_KEY')
cx = st.secrets.get('google_search', {}).get('CX')

if api_key and cx:
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q=002183+股票+新闻&num=3"
    
    try:
        response = requests.get(url, timeout=10)
        st.write(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ 获取到 {len(data.get('items', []))} 条结果")
            st.json(data)
        else:
            st.error(f"❌ 错误: {response.text[:500]}")
    except Exception as e:
        st.error(f"❌ 异常: {e}")
else:
    st.error("❌ 配置未找到")
```

---

## ⚡ 最快速的解决方案

### 如果上述都不行，使用 OpenAI 作为新闻源

将您的 Secrets 改为：

```toml
[llm]
OPENAI_API_KEY = "sk-OQ6xiwqyiXYUpzNWe...........QSdJnQk"
OPENAI_API_BASE = "https://coultra.blueshirtmap.com/v1"

# 启用 OpenAI 作为新闻源（优先级高）
OPENAI_NEWS_ENABLED = "true"

[data_sources]
FINNHUB_API_KEY = "ctt5209r01qin3c1au......r01qin3c1auag"
```

系统会自动使用 OpenAI 进行新闻搜索（虽然会消耗一些 token，但肯定能工作）。

---

## 🎯 问题排查清单

请逐项确认：

- [ ] Streamlit Cloud Secrets 已添加 `[google_search]` section
- [ ] API_KEY 和 CX 值正确（无多余空格）
- [ ] 保存 Secrets 后等待了30秒以上
- [ ] 已刷新浏览器页面
- [ ] 应用已重启（查看部署日志）
- [ ] 最新代码已部署（commit f1c71b7）
- [ ] 在浏览器中测试 API URL 能返回数据
- [ ] 查看了应用日志，搜索 `[Google Custom Search]`

---

## 📞 立即行动步骤

### 立即执行（按顺序）：

1. **复制测试配置**：
   ```toml
   [google_search]
   API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
   CX = "c09a7a52c4c364088"
   ```

2. **粘贴到 Streamlit Secrets** → Save

3. **等待30秒** → 刷新页面

4. **测试分析股票 002183**

5. **如果仍然失败**：
   - 截图 Secrets 配置（隐藏敏感信息）
   - 截图应用日志（搜索 `[Google Custom Search]` 或 `[统一新闻工具]`）
   - 提供浏览器测试 API URL 的结果

---

## 💡 常见错误和解决

### 错误1：拼写错误

❌ **错误**：
```toml
[google_search]
APIKEY = "xxx"  # 少了下划线
```

✅ **正确**：
```toml
[google_search]
API_KEY = "xxx"
```

### 错误2：缺少引号

❌ **错误**：
```toml
[google_search]
API_KEY = AIzaSyXXX  # 没有引号
```

✅ **正确**：
```toml
[google_search]
API_KEY = "AIzaSyXXX"
```

### 错误3：多余的空格

❌ **错误**：
```toml
[google_search]
API_KEY = " AIzaSyXXX "  # 前后有空格
```

✅ **正确**：
```toml
[google_search]
API_KEY = "AIzaSyXXX"  # 无多余空格
```

---

## 🆘 终极方案

如果一切都失败了，请提供：

1. **Secrets 配置截图**（隐藏密钥后半部分）
2. **应用日志**（搜索 `[Google Custom Search]` 相关内容）
3. **浏览器 API 测试结果**
4. **调试代码的输出截图**

我会根据这些信息为您定制解决方案！

---

**现在就去 Streamlit Cloud 添加测试配置吧！** 🚀

