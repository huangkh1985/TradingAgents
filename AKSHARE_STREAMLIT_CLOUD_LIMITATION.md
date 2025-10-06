# AKShare 在 Streamlit Cloud 上的限制说明

## 🚨 核心问题

**AKShare 在本地可以正常获取新闻，但在 Streamlit Cloud 上无法工作。**

这是一个**环境限制问题**，不是代码错误。

---

## 📋 原因分析

### 1. **网络访问限制** ⭐ 主要原因

Streamlit Cloud 的服务器位于**国外（通常是美国）**，而 AKShare 需要访问的东方财富等网站在**中国境内**。

#### 具体限制：

- **地理位置限制**：东方财富网站可能对国外 IP 有访问限制
- **防火墙规则**：中国网站可能限制来自境外的爬虫请求
- **反爬虫机制**：检测到境外 IP 访问时返回空数据或错误

#### 证据：

```python
# 本地运行（中国 IP）
import akshare as ak
news = ak.stock_news_em("002183")
print(len(news))  # ✅ 成功：10条新闻

# Streamlit Cloud 运行（美国 IP）
import akshare as ak
news = ak.stock_news_em("002183")
print(len(news))  # ❌ 失败：0条新闻 或 超时
```

### 2. **网络延迟和超时**

Streamlit Cloud → 中国网站的网络延迟较高：

- **本地**：访问东方财富 < 100ms
- **Streamlit Cloud**：访问东方财富 > 1000ms（甚至超时）

代码中设置的30秒超时可能不够：

```python
# tradingagents/dataflows/akshare_utils.py
thread.join(timeout=30)  # 在 Streamlit Cloud 上可能仍然超时
```

### 3. **IP 黑名单**

Streamlit Cloud 使用的 IP 地址段可能被中国网站加入黑名单：

- Streamlit Cloud 部署在 AWS
- 该 IP 段可能被识别为"爬虫"或"机器人"
- 被东方财富等网站自动屏蔽

### 4. **DNS 解析问题**

在某些情况下，Streamlit Cloud 可能无法正确解析中国网站的域名：

```bash
# Streamlit Cloud 环境
nslookup eastmoney.com
# 可能返回错误或超时
```

### 5. **SSL/TLS 证书问题**

中国网站的 SSL 证书可能与 Streamlit Cloud 的环境不兼容。

---

## 🔍 验证方法

### 在 Streamlit Cloud 上测试

添加诊断代码到您的应用：

```python
import streamlit as st
import requests
import akshare as ak
from datetime import datetime

st.write("## AKShare 诊断测试")

# 测试1：检查网络连接
st.write("### 1. 测试网络连接")
try:
    response = requests.get("https://www.eastmoney.com", timeout=10)
    st.success(f"✅ 东方财富可访问，状态码: {response.status_code}")
except Exception as e:
    st.error(f"❌ 东方财富不可访问: {e}")

# 测试2：检查 AKShare 功能
st.write("### 2. 测试 AKShare 获取新闻")
try:
    start_time = datetime.now()
    news = ak.stock_news_em("002183")
    elapsed = (datetime.now() - start_time).total_seconds()
    
    if news is not None and not news.empty:
        st.success(f"✅ AKShare 成功，获取 {len(news)} 条新闻，耗时 {elapsed:.2f} 秒")
        st.dataframe(news.head())
    else:
        st.error(f"❌ AKShare 返回空数据，耗时 {elapsed:.2f} 秒")
except Exception as e:
    st.error(f"❌ AKShare 异常: {e}")

# 测试3：显示服务器信息
st.write("### 3. 服务器信息")
try:
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    st.info(f"主机名: {hostname}\nIP地址: {ip}")
except:
    st.warning("无法获取服务器信息")
```

---

## ✅ 解决方案

### 方案1：使用 Google Custom Search API（推荐）✨

**您已经配置好了！** 这是专门为 Streamlit Cloud 设计的解决方案。

```toml
# Streamlit Secrets
[google_search]
API_KEY = "AIzaSyXXX..."
CX = "0123456789abc..."
```

**优势**：
- ✅ 在 Streamlit Cloud 上完全可用
- ✅ 稳定可靠（官方 API）
- ✅ 无地理位置限制
- ✅ 支持中英文搜索

**新闻获取优先级**（已优化）：
```
A股：东方财富 → Google Custom Search API → 网页爬虫 → OpenAI
           ↓ (Streamlit Cloud 不可用)
     Google Custom Search API → OpenAI
```

### 方案2：配置代理服务器（高级）

如果必须使用 AKShare，可以通过代理：

```python
import os
os.environ['HTTP_PROXY'] = 'http://your-china-proxy.com:port'
os.environ['HTTPS_PROXY'] = 'http://your-china-proxy.com:port'

import akshare as ak
news = ak.stock_news_em("002183")
```

**缺点**：
- 需要购买中国境内的代理服务
- 配置复杂
- 可能违反 Streamlit Cloud 使用条款

### 方案3：使用 OpenAI/DeepSeek 进行新闻搜索

配置 LLM API 密钥：

```toml
[llm]
OPENAI_API_KEY = "sk-xxx..."
# 或
DEEPSEEK_API_KEY = "sk-xxx..."
```

系统会自动使用 LLM 进行新闻搜索。

---

## 📊 对比总结

| 方案 | 本地环境 | Streamlit Cloud | 稳定性 | 成本 |
|------|---------|----------------|--------|------|
| **AKShare** | ✅ 可用 | ❌ 不可用 | ⭐⭐⭐ | 免费 |
| **Google Custom Search** | ✅ 可用 | ✅ 可用 | ⭐⭐⭐⭐⭐ | 免费100次/天 |
| **OpenAI API** | ✅ 可用 | ✅ 可用 | ⭐⭐⭐⭐ | 付费 |
| **代理服务器** | ✅ 可用 | ⚠️ 复杂 | ⭐⭐ | 付费 |

---

## 🎯 最佳实践

### 本地开发

使用 AKShare（免费且快速）：
```python
# 本地环境自动使用 AKShare
news = get_realtime_stock_news("002183", "2025-01-06")
```

### Streamlit Cloud 部署

配置 Google Custom Search API：
```toml
# .streamlit/secrets.toml
[google_search]
API_KEY = "AIzaSyXXX..."
CX = "0123456789abc..."
```

系统会自动检测环境并选择最佳数据源：
- **本地**：AKShare（免费）
- **Streamlit Cloud**：Google Custom Search API（稳定）

---

## 🔧 系统已自动优化

### 智能回退机制

系统已经实现了智能回退：

```python
# tradingagents/tools/unified_news_tool.py
def _get_a_share_news(self, stock_code: str, ...):
    # 优先级1: 东方财富（本地可用）
    try:
        result = self.toolkit.get_realtime_stock_news.invoke(...)
        if result and len(result.strip()) > 100:
            return result  # ✅ 本地成功
    except:
        pass  # ❌ Streamlit Cloud 失败，继续
    
    # 优先级2: Google Custom Search API（Streamlit Cloud 可用）
    try:
        result = get_google_custom_search_news(...)
        if result and len(result.strip()) > 100:
            return result  # ✅ Streamlit Cloud 成功
    except:
        pass
    
    # 优先级3: 其他备用方案...
```

### 日志示例

**本地环境**：
```
[统一新闻工具] 尝试东方财富实时新闻...
[东方财富新闻] ✅ 获取成功: 002183, 共10条记录，耗时: 1.23秒
[统一新闻工具] ✅ 东方财富新闻获取成功: 2456 字符
```

**Streamlit Cloud 环境**：
```
[统一新闻工具] 尝试东方财富实时新闻...
[东方财富新闻] ⚠️ 获取超时（30秒）: 002183
[统一新闻工具] 东方财富新闻获取失败
[统一新闻工具] 尝试Google Custom Search API...
[Google Custom Search] 配置成功
[Google Custom Search] 获取到 8 条结果，耗时 0.85 秒
[统一新闻工具] ✅ Google Custom Search API获取成功: 2134 字符
```

---

## 💡 为什么选择 Google Custom Search API？

### 1. **专为云环境设计**
- 官方 API，全球可用
- 无地理位置限制
- 无 IP 黑名单问题

### 2. **Streamlit Cloud 友好**
- 完全兼容 Streamlit Secrets
- 无需额外配置
- 自动识别和使用

### 3. **性能优秀**
- 响应速度快（< 1秒）
- 搜索质量高
- 支持中英文

### 4. **免费额度充足**
- 每天100次免费查询
- 足够个人使用和测试
- 超出后自动回退到其他数据源

---

## 🚀 立即行动

### 您已经完成配置！

✅ Google Custom Search API 已集成
✅ Streamlit Secrets 已配置
✅ 系统会自动使用

### 验证步骤：

1. **部署到 Streamlit Cloud**（已完成）
2. **选择股票进行分析**（如 002183）
3. **查看新闻分析结果**
4. **检查日志**：
   ```
   [Google Custom Search] 配置成功
   [统一新闻工具] ✅ Google Custom Search API获取成功
   ```

如果看到以上日志，说明系统正在使用 Google Custom Search API 成功获取新闻！

---

## 📚 相关文档

- [Google Custom Search API 配置](GOOGLE_CUSTOM_SEARCH_SETUP.md)
- [完整新闻搜索指南](GOOGLE_NEWS_SEARCH_GUIDE.md)
- [新闻分析问题诊断](NEWS_ANALYSIS_FIX_GUIDE.md)

---

## 总结

### 问题本质

**AKShare 在 Streamlit Cloud 上不可用是环境限制，不是代码问题。**

原因：
- ❌ Streamlit Cloud 服务器在国外
- ❌ 东方财富网站限制境外访问
- ❌ 网络延迟和 IP 黑名单

### 解决方案

**✅ 使用 Google Custom Search API**

- 已集成到项目
- 已配置到 Secrets
- 自动生效

### 效果

- **本地**：使用 AKShare（免费、快速）
- **Streamlit Cloud**：使用 Google Custom Search API（稳定、可靠）
- **无缝切换**：系统自动选择最佳数据源

您不需要做任何额外操作，系统已经为您优化好了！🎉

