# Google 新闻搜索配置指南

## 📋 目录
- [当前实现方式](#当前实现方式)
- [方案1：网页爬虫（当前使用）](#方案1网页爬虫当前使用)
- [方案2：Google Custom Search API](#方案2google-custom-search-api)
- [方案3：使用Google AI进行新闻搜索](#方案3使用google-ai进行新闻搜索)
- [对比与建议](#对比与建议)

---

## 当前实现方式

TradingAgents **目前使用的是网页爬虫方式**获取Google新闻，而非Google Search API。

### 实现原理

```python
# tradingagents/dataflows/googlenews_utils.py
def getNewsData(query, start_date, end_date):
    """
    通过网页爬虫获取Google新闻搜索结果
    """
    url = (
        f"https://www.google.com/search?q={query}"
        f"&tbs=cdr:1,cd_min:{start_date},cd_max:{end_date}"
        f"&tbm=nws&start={offset}"
    )
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # 解析HTML获取新闻数据
```

### 特点

✅ **优点**：
- 无需API密钥
- 完全免费
- 无请求次数限制
- 支持中文搜索

❌ **缺点**：
- 可能被Google限流或封IP
- HTML结构变化时需要更新解析逻辑
- 在某些环境下可能被阻止（如Streamlit Cloud）
- 不太稳定

---

## 方案1：网页爬虫（当前使用）

### 如何使用

当前系统已经集成，**无需额外配置**，直接使用即可：

```python
from tradingagents.dataflows.interface import get_google_news

# 获取新闻
news = get_google_news(
    query="002183 股票 新闻 财报 业绩",  # 搜索查询
    curr_date="2025-01-06",              # 截止日期
    look_back_days=7                      # 回溯天数
)

print(news)
```

### 常见问题

#### 问题1：在Streamlit Cloud上无法使用

**原因**：Streamlit Cloud可能限制网页爬虫

**解决方案**：使用方案2或方案3

#### 问题2：被Google限流

**症状**：
```
requests.exceptions.HTTPError: 429 Too Many Requests
```

**解决方案**：
1. 减少请求频率
2. 使用代理IP
3. 切换到Google Custom Search API（方案2）

---

## 方案2：Google Custom Search API

如果网页爬虫不稳定，可以使用官方的Google Custom Search API。

### 步骤1：创建Google Cloud项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **Custom Search API**

### 步骤2：创建自定义搜索引擎

1. 访问 [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. 点击"添加"创建新的搜索引擎
3. 配置：
   - **搜索内容**：选择"搜索整个网络"
   - **名称**：TradingAgents News Search
   - **语言**：中文和英文
4. 创建后，记录 **搜索引擎ID（CX）**

### 步骤3：获取API密钥

1. 在 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. 创建凭据 → API密钥
3. 记录 **API密钥**

### 步骤4：配置到项目

```bash
# .env 文件
GOOGLE_CUSTOM_SEARCH_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GOOGLE_CUSTOM_SEARCH_CX=0123456789abcdefg:xxxxxxxxxx
```

或在 Streamlit Cloud Secrets 中：

```toml
# .streamlit/secrets.toml
[google_search]
API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CX = "0123456789abcdefg:xxxxxxxxxx"
```

### 步骤5：实现代码

创建 `tradingagents/dataflows/google_custom_search.py`：

```python
#!/usr/bin/env python3
"""
Google Custom Search API 新闻搜索
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class GoogleCustomSearchNews:
    """使用Google Custom Search API获取新闻"""
    
    def __init__(self):
        # 从环境变量或Streamlit Secrets获取
        self.api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
        self.cx = os.getenv('GOOGLE_CUSTOM_SEARCH_CX')
        
        # 尝试从Streamlit Secrets读取
        if not self.api_key or not self.cx:
            try:
                import streamlit as st
                self.api_key = st.secrets.get('google_search', {}).get('API_KEY')
                self.cx = st.secrets.get('google_search', {}).get('CX')
            except:
                pass
        
        if not self.api_key or not self.cx:
            logger.warning("Google Custom Search API未配置")
    
    def search_news(
        self, 
        query: str, 
        start_date: str, 
        end_date: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        搜索新闻
        
        Args:
            query: 搜索查询
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            max_results: 最大结果数
            
        Returns:
            新闻列表
        """
        if not self.api_key or not self.cx:
            logger.error("Google Custom Search API未配置")
            return []
        
        # 构建API请求
        url = "https://www.googleapis.com/customsearch/v1"
        
        # 转换日期格式
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # 构建日期范围参数
        date_restrict = f"d{(end - start).days}"  # 最近N天
        
        params = {
            'key': self.api_key,
            'cx': self.cx,
            'q': query,
            'num': min(max_results, 10),  # 每次最多10个结果
            'dateRestrict': date_restrict,
            'sort': 'date',  # 按日期排序
            'tbm': 'nws'  # 新闻搜索
        }
        
        try:
            logger.info(f"[Google Custom Search] 搜索: {query}, 日期: {start_date} 至 {end_date}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('items', [])
            
            news_list = []
            for item in items:
                news_list.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': item.get('displayLink', ''),
                    'date': item.get('pagemap', {}).get('metatags', [{}])[0].get('article:published_time', '')
                })
            
            logger.info(f"[Google Custom Search] 获取到 {len(news_list)} 条新闻")
            return news_list
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error("[Google Custom Search] API配额已用完")
            else:
                logger.error(f"[Google Custom Search] HTTP错误: {e}")
            return []
        except Exception as e:
            logger.error(f"[Google Custom Search] 搜索失败: {e}")
            return []


def get_google_custom_search_news(query: str, curr_date: str, look_back_days: int = 7) -> str:
    """
    使用Google Custom Search API获取新闻
    """
    searcher = GoogleCustomSearchNews()
    
    # 计算日期范围
    end_date = datetime.strptime(curr_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=look_back_days)
    
    # 搜索新闻
    news_list = searcher.search_news(
        query=query,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=curr_date,
        max_results=10
    )
    
    if not news_list:
        return ""
    
    # 格式化输出
    news_str = ""
    for news in news_list:
        news_str += f"### {news['title']} (来源: {news['source']})\n\n"
        news_str += f"{news['snippet']}\n\n"
        news_str += f"🔗 {news['link']}\n\n"
    
    return f"## {query} Google News ({start_date.strftime('%Y-%m-%d')} 至 {curr_date}):\n\n{news_str}"
```

### 步骤6：修改统一新闻工具

编辑 `tradingagents/tools/unified_news_tool.py`，在 `_get_a_share_news` 方法中添加：

```python
# 优先级2: Google Custom Search API
try:
    from tradingagents.dataflows.google_custom_search import get_google_custom_search_news
    logger.info(f"[统一新闻工具] 尝试Google Custom Search API...")
    query = f"{stock_code} 股票 新闻 财报 业绩"
    result = get_google_custom_search_news(query, curr_date)
    if result and len(result.strip()) > 50:
        logger.info(f"[统一新闻工具] ✅ Google Custom Search API获取成功")
        return self._format_news_result(result, "Google Custom Search", model_info)
except Exception as e:
    logger.warning(f"[统一新闻工具] Google Custom Search API失败: {e}")
```

### API配额限制

Google Custom Search API 限制：
- **免费版**：每天100次查询
- **付费版**：$5/1000次查询

---

## 方案3：使用Google AI进行新闻搜索

如果您已经配置了Google AI（Gemini），可以利用其联网搜索能力。

### 配置Google AI API

```bash
# .env 文件
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

或 Streamlit Cloud Secrets：

```toml
[llm]
GOOGLE_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### 实现代码

```python
import google.generativeai as genai
import os

# 配置API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# 创建模型（使用支持grounding的版本）
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# 使用Google Search grounding
response = model.generate_content(
    f"搜索关于股票002183（怡亚通）的最新新闻和财报信息",
    tools='google_search_retrieval'  # 启用Google搜索
)

print(response.text)
```

### 注意事项

- 需要 Google AI Studio API 密钥（与Custom Search不同）
- Grounding功能可能有地区限制
- 不是所有Gemini模型都支持grounding

---

## 对比与建议

### 功能对比

| 特性 | 网页爬虫 | Custom Search API | Google AI Grounding |
|------|---------|------------------|-------------------|
| **费用** | 免费 | 免费100次/天<br>付费$5/1000次 | 根据token计费 |
| **稳定性** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **速度** | 快 | 中等 | 慢 |
| **配置难度** | 低 | 中 | 低 |
| **Streamlit Cloud** | ❌ 可能不可用 | ✅ 可用 | ✅ 可用 |
| **请求限制** | 易被限流 | 100次/天（免费） | 根据API配额 |
| **中文支持** | ✅ 好 | ✅ 好 | ✅ 好 |

### 推荐方案

#### 本地开发环境
```
方案1（网页爬虫）→ 免费，够用
```

#### Streamlit Cloud环境
```
方案2（Custom Search API）→ 最稳定
或
方案3（Google AI）→ 如果已配置Google AI
```

#### 生产环境
```
方案2（Custom Search API付费版）→ 最可靠
```

---

## 快速配置指南

### 选择1：继续使用网页爬虫（最简单）

✅ **无需配置**，当前已集成

⚠️ 注意：
- 在Streamlit Cloud可能不可用
- 可能被Google限流

### 选择2：配置Google Custom Search API（推荐）

1. **创建搜索引擎**：https://programmablesearchengine.google.com/
2. **获取API密钥**：https://console.cloud.google.com/apis/credentials
3. **配置环境变量**：
   ```bash
   GOOGLE_CUSTOM_SEARCH_API_KEY=xxx
   GOOGLE_CUSTOM_SEARCH_CX=xxx
   ```
4. **添加实现代码**（见方案2步骤5）

### 选择3：使用Google AI（如果已配置）

1. **获取API密钥**：https://makersuite.google.com/app/apikey
2. **配置环境变量**：
   ```bash
   GOOGLE_API_KEY=AIzaSyXXX...
   ```
3. **系统自动使用**（已集成Google AI LLM）

---

## 故障排除

### 问题1：网页爬虫返回空结果

```python
# 检查是否被Google限流
import requests
response = requests.get("https://www.google.com/search?q=test&tbm=nws")
print(response.status_code)  # 200正常，429被限流
```

**解决**：
- 等待一段时间
- 切换到Custom Search API

### 问题2：Custom Search API返回403

**原因**：API密钥未启用Custom Search API

**解决**：
1. 访问 https://console.cloud.google.com/apis/library/customsearch.googleapis.com
2. 点击"启用"

### 问题3：Custom Search API返回429

**原因**：超出每日配额（免费100次）

**解决**：
- 等待明天重置
- 升级到付费版
- 使用网页爬虫作为备用

---

## 总结

### 当前状态

✅ TradingAgents **当前使用网页爬虫**获取Google新闻
- 无需配置
- 完全免费
- 可能不稳定

### 升级建议

如果遇到以下情况，建议切换到Google Custom Search API：
- ✅ 在Streamlit Cloud部署
- ✅ 需要稳定的生产环境
- ✅ 经常被Google限流
- ✅ 有预算（$5/1000次查询）

### 配置优先级

1. **本地开发**：网页爬虫（当前）
2. **Streamlit Cloud**：Custom Search API 或 Google AI
3. **生产环境**：Custom Search API（付费）

---

## 参考链接

- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
- [Google Custom Search API文档](https://developers.google.com/custom-search/v1/overview)
- [Google AI Studio](https://makersuite.google.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

