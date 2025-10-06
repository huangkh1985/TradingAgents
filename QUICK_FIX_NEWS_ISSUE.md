# 新闻获取问题快速修复指南

## 🚨 问题现象

在 Streamlit Cloud 上运行股票分析（如 002183）时，新闻分析模块提示：
```
📰 新闻事件分析
我将为您分析股票代码002183的最新新闻情况。
让我先获取相关的新闻数据。
→ 仍然没有获取到新闻
```

## 🔍 立即诊断

### 步骤1：检查 Streamlit Cloud Secrets 配置

请确认您的 Streamlit Cloud Secrets 配置**完全正确**：

#### ✅ 正确的配置格式（三选一）

**方式1：使用 google_search section**（推荐）
```toml
[google_search]
API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
CX = "c09a7a52c4c364088"
```

**方式2：直接配置**
```toml
GOOGLE_CUSTOM_SEARCH_API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
GOOGLE_CUSTOM_SEARCH_CX = "c09a7a52c4c364088"
```

**方式3：在 llm section 中**
```toml
[llm]
GOOGLE_CUSTOM_SEARCH_API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
GOOGLE_CUSTOM_SEARCH_CX = "c09a7a52c4c364088"
```

#### ❌ 常见错误

```toml
# 错误1：拼写错误
[google_search]
APIKEY = "xxx"  # ❌ 应该是 API_KEY
CX = "xxx"

# 错误2：缺少引号
[google_search]
API_KEY = AIzaSyXXX  # ❌ 应该加引号
CX = "xxx"

# 错误3：多余的空格
[google_search]
API_KEY = " AIzaSyXXX "  # ❌ 不要有前后空格
CX = "xxx"

# 错误4：使用了错误的key
GOOGLE_SEARCH_API_KEY = "xxx"  # ❌ 应该是 GOOGLE_CUSTOM_SEARCH_API_KEY
```

### 步骤2：验证 API Key 和 CX

#### 检查 API Key 格式
- ✅ 应该以 `AIza` 开头
- ✅ 长度约 39 个字符
- ✅ 只包含字母、数字、下划线和连字符

#### 检查 CX（搜索引擎ID）格式
- ✅ 格式：`数字字母:数字字母`
- ✅ 示例：`c09a7a52c4c364088` 或 `017576662512468239146:omuauf_lfve`

#### 手动测试 API

在浏览器中打开以下 URL（替换您的 API_KEY 和 CX）：

```
https://www.googleapis.com/customsearch/v1?key=YOUR_API_KEY&cx=YOUR_CX&q=002183+股票+新闻&num=3
```

如果返回 JSON 数据（包含 `items` 数组），说明配置正确。

### 步骤3：检查 API 是否启用

1. 访问 [Google Cloud Console - Custom Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com)
2. 确保状态显示"已启用"
3. 如果显示"启用"按钮，点击启用

### 步骤4：检查搜索引擎配置

1. 访问 [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. 找到您的搜索引擎
3. 点击"控制面板"
4. 确认：
   - ✅ "搜索整个网络"已开启
   - ✅ 状态：已启用
   - ✅ 搜索引擎 ID（CX）正确复制

## 🛠️ 快速修复方案

### 方案A：使用测试配置（验证功能）

暂时使用这个测试配置验证功能是否正常：

```toml
[google_search]
API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
CX = "c09a7a52c4c364088"
```

**注意**：这是测试配置，有配额限制。验证后请替换为您自己的配置。

### 方案B：使用 OpenAI API（备用方案）

如果 Google Custom Search 配置有问题，可以暂时使用 OpenAI：

```toml
[llm]
OPENAI_API_KEY = "sk-您的OpenAI密钥"
OPENAI_API_BASE = "https://coultra.blueshirtmap.com/v1"
```

系统会自动使用 OpenAI 进行新闻搜索。

### 方案C：使用 Google AI（如果已配置）

```toml
[llm]
GOOGLE_API_KEY = "AIza您的GoogleAI密钥"
```

系统会使用 Google AI 的 grounding 功能搜索新闻。

## 📋 完整的 Secrets 配置示例

### 推荐配置（包含所有功能）

```toml
# ===== LLM 配置 =====
[llm]
# OpenAI（主要LLM）
OPENAI_API_KEY = "sk-OQ6xiwqyiXYUpzNWe...........QSdJnQk"
OPENAI_API_BASE = "https://coultra.blueshirtmap.com/v1"

# DeepSeek（备用LLM）
DEEPSEEK_API_KEY = "sk-96af8f5cea7...........5dbe08"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Google AI（可选）
GOOGLE_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# ===== Google 新闻搜索配置 =====
[google_search]
API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
CX = "c09a7a52c4c364088"

# ===== 数据源配置 =====
[data_sources]
FINNHUB_API_KEY = "ctt5209r01qin3c1au......r01qin3c1auag"
```

## 🔧 调试步骤

### 1. 添加调试代码

在您的 Streamlit 应用中临时添加：

```python
import streamlit as st
import os

st.write("## 🔍 配置诊断")

# 检查 Secrets
if hasattr(st, 'secrets'):
    st.write("### Streamlit Secrets 状态:")
    
    # 检查 google_search section
    if 'google_search' in st.secrets:
        api_key = st.secrets['google_search'].get('API_KEY')
        cx = st.secrets['google_search'].get('CX')
        st.success(f"✅ google_search section 存在")
        st.write(f"- API_KEY: {api_key[:20] if api_key else '未配置'}...")
        st.write(f"- CX: {cx[:15] if cx else '未配置'}...")
    else:
        st.error("❌ google_search section 不存在")
    
    # 检查直接配置
    api_key_direct = st.secrets.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
    cx_direct = st.secrets.get('GOOGLE_CUSTOM_SEARCH_CX')
    
    if api_key_direct:
        st.info(f"ℹ️ 找到 GOOGLE_CUSTOM_SEARCH_API_KEY: {api_key_direct[:20]}...")
    if cx_direct:
        st.info(f"ℹ️ 找到 GOOGLE_CUSTOM_SEARCH_CX: {cx_direct[:15]}...")
    
    # 测试 API
    if (api_key := st.secrets.get('google_search', {}).get('API_KEY') or 
                   st.secrets.get('GOOGLE_CUSTOM_SEARCH_API_KEY')):
        if (cx := st.secrets.get('google_search', {}).get('CX') or 
                 st.secrets.get('GOOGLE_CUSTOM_SEARCH_CX')):
            
            st.write("### 测试 Google Custom Search API:")
            import requests
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cx,
                'q': '002183 股票 新闻',
                'num': 3
            }
            
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    st.success(f"✅ API 测试成功！获取到 {len(items)} 条结果")
                    if items:
                        st.write("结果示例:")
                        for i, item in enumerate(items[:2], 1):
                            st.write(f"{i}. {item.get('title', 'N/A')}")
                else:
                    st.error(f"❌ API 返回错误: {response.status_code}")
                    st.code(response.text[:500])
            except Exception as e:
                st.error(f"❌ API 测试失败: {e}")
else:
    st.error("❌ Streamlit Secrets 不可用")
```

### 2. 查看日志

在 Streamlit Cloud 应用界面右下角点击"Manage app" → "Logs"，查找：

```
[Google Custom Search] 配置成功
[Google Custom Search] 获取到 X 条结果
```

或者查找错误：

```
[Google Custom Search] API未配置
[Google Custom Search] API错误
```

## 🎯 最终检查清单

在确认修复前，请逐项检查：

- [ ] Google Custom Search API 已在 Google Cloud Console 中启用
- [ ] API 密钥格式正确（以 `AIza` 开头）
- [ ] CX（搜索引擎 ID）格式正确
- [ ] Streamlit Secrets 配置正确（无拼写错误）
- [ ] 搜索引擎配置为"搜索整个网络"
- [ ] 使用浏览器测试 API URL 能返回数据
- [ ] 在 Streamlit 应用中添加了调试代码
- [ ] 重启了 Streamlit Cloud 应用
- [ ] 查看了应用日志

## 📞 仍然无法解决？

### 提供以下信息以便诊断：

1. **调试输出截图**（添加上面的调试代码后的输出）
2. **Streamlit Cloud 日志**（搜索 `[Google Custom Search]` 或 `[统一新闻工具]`）
3. **Secrets 配置**（隐藏敏感信息）：
   ```toml
   [google_search]
   API_KEY = "AIzaSy...（隐藏）"
   CX = "c09a7...（隐藏）"
   ```
4. **浏览器测试 API 的结果**

### 临时解决方案

如果急需使用，可以暂时：

1. **使用 OpenAI API**（如果已配置）- 系统会自动用 OpenAI 搜索新闻
2. **本地运行**（使用 AKShare）- 本地环境新闻功能正常
3. **等待技术支持** - 提供诊断信息后获得帮助

## 🚀 预防措施

为避免以后出现问题：

1. **保存配置备份**：将 Secrets 配置保存到本地文件
2. **定期测试**：使用浏览器 URL 定期测试 API 是否正常
3. **监控配额**：Google Custom Search 免费版每天 100 次
4. **配置告警**：当 API 失败时接收通知

---

## 💡 常见解决方案

### 问题：配置了但仍然说"未配置"

**原因**：Streamlit 缓存问题

**解决**：
1. 在 Streamlit Cloud 后台点击"Reboot app"
2. 或者修改 secrets 后等待 30 秒自动重启

### 问题：API 返回 403

**原因**：API 未启用

**解决**：
1. 访问 https://console.cloud.google.com/apis/library/customsearch.googleapis.com
2. 点击"启用"

### 问题：API 返回 429

**原因**：超出配额（100次/天）

**解决**：
1. 等待第二天配额重置
2. 或升级到付费版
3. 或使用其他新闻源（OpenAI）

---

**立即行动**：
1. 检查 Secrets 配置格式
2. 添加调试代码
3. 重启应用
4. 查看调试输出
5. 根据结果进行修复

祝您顺利解决问题！🎉

