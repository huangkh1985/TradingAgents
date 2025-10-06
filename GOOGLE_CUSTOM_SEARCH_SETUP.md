# Google Custom Search API 配置与使用说明

## ✅ 功能已集成

Google Custom Search API 已成功集成到 TradingAgents 新闻搜索系统中。

## 📋 Streamlit Cloud 配置方式

### 方式1：使用 `google_search` section（推荐）

在 Streamlit Cloud 的 Secrets 中添加：

```toml
[google_search]
API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CX = "0123456789abcdefg:xxxxxxxxxx"
```

### 方式2：使用独立配置项

```toml
GOOGLE_CUSTOM_SEARCH_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
GOOGLE_CUSTOM_SEARCH_CX = "0123456789abcdefg:xxxxxxxxxx"
```

## 🔧 如何获取 API Key 和 CX

### 步骤1：创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目

### 步骤2：启用 Custom Search API

1. 访问 [Custom Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com)
2. 点击"启用"按钮

### 步骤3：创建 API 密钥

1. 访问 [API凭据页面](https://console.cloud.google.com/apis/credentials)
2. 点击"创建凭据" → "API密钥"
3. 复制生成的 API 密钥（以 `AIza` 开头）

### 步骤4：创建自定义搜索引擎

1. 访问 [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. 点击"添加"创建新搜索引擎
3. 配置：
   - **搜索内容**：选择"搜索整个网络"
   - **名称**：TradingAgents News Search
   - **语言**：中文和英文
4. 创建后，点击"控制面板"
5. 在"基本信息"中找到**搜索引擎ID（CX）**
   - 格式：`0123456789abcdefg:xxxxxxxxxx`

## 📊 新闻获取优先级

### A股新闻
1. ✅ **东方财富实时新闻**（AKShare）
2. ✅ **Google Custom Search API**（新增！）
3. Google 新闻（网页爬虫）
4. OpenAI 全球新闻

### 港股新闻
1. ✅ **Google Custom Search API**（新增！）
2. Google 新闻（网页爬虫）
3. OpenAI 全球新闻
4. 实时新闻

### 美股新闻
1. ✅ **Google Custom Search API**（新增！）
2. OpenAI 全球新闻
3. Google 新闻（网页爬虫）
4. FinnHub 新闻

## 🔍 测试配置

### 方法1：使用诊断脚本

```bash
python scripts/diagnose_news_sources.py
```

这会自动检测：
- Google Custom Search API 是否配置
- API 密钥是否有效
- 搜索功能是否正常

### 方法2：手动测试

```python
from tradingagents.dataflows.google_custom_search import get_google_custom_search_news

# 测试A股新闻搜索
result = get_google_custom_search_news(
    query="002183 股票 新闻 财报",
    curr_date="2025-01-06",
    look_back_days=7
)

if result:
    print("✅ Google Custom Search API 工作正常！")
    print(result[:500])
else:
    print("❌ 未获取到新闻，请检查配置")
```

## 💰 API 配额限制

### 免费版
- **每天100次查询**
- 完全免费
- 适合个人使用和测试

### 付费版
- **$5 / 1000次查询**
- 无每日限制
- 适合生产环境

## ⚙️ 配置示例

### 完整的 Streamlit Cloud Secrets 配置

```toml
# LLM 配置
[llm]
OPENAI_API_KEY = "sk-xxx..."
GOOGLE_API_KEY = "AIza..."  # Google AI（Gemini）
DEEPSEEK_API_KEY = "sk-xxx..."

# Google Search 配置（新增）
[google_search]
API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Google Custom Search API Key
CX = "0123456789abcdefg:xxxxxxxxxx"              # 搜索引擎ID

# 数据源配置
[data_sources]
FINNHUB_API_KEY = "ctt5209r01qin3c1auag"
```

## 🚀 使用效果

配置后，系统会：

1. **自动检测**：首先尝试使用 Google Custom Search API
2. **稳定可靠**：官方 API，不会被限流
3. **智能回退**：如果 API 未配置或失败，自动使用其他新闻源
4. **详细日志**：记录每个新闻源的尝试结果

### 日志示例

```
[统一新闻工具] 获取A股 002183 新闻
[统一新闻工具] 尝试东方财富实时新闻...
[统一新闻工具] ⚠️ 东方财富新闻内容过短或为空
[统一新闻工具] 尝试Google Custom Search API...
[Google Custom Search] 配置成功: API Key=AIzaSyXXXXXXXXXXXXXX..., CX=0123456789abc...
[Google Custom Search] 开始搜索: '002183 股票 新闻 财报 业绩', 日期范围: 2024-12-30 至 2025-01-06
[Google Custom Search] 获取到 8 条结果，耗时 0.85 秒
[统一新闻工具] ✅ Google Custom Search API获取成功: 2456 字符
```

## ❓ 常见问题

### Q1: API 返回 403 错误

**原因**：API 密钥未启用 Custom Search API

**解决**：
1. 访问 https://console.cloud.google.com/apis/library/customsearch.googleapis.com
2. 点击"启用"

### Q2: API 返回 429 错误

**原因**：超出每日配额（免费版100次）

**解决**：
- 等待明天配额重置
- 升级到付费版
- 系统会自动回退到其他新闻源

### Q3: 搜索结果为空

**可能原因**：
1. 搜索引擎配置错误（未选择"搜索整个网络"）
2. 搜索查询太具体
3. 日期范围内确实没有相关新闻

**解决**：
1. 检查搜索引擎配置
2. 查看日志了解具体原因
3. 系统会自动尝试其他新闻源

### Q4: 如何查看是否使用了 Google Custom Search API？

查看应用日志，搜索：
```
[Google Custom Search]
[统一新闻工具] ✅ Google Custom Search API获取成功
```

## 📚 相关文档

- [完整配置指南](GOOGLE_NEWS_SEARCH_GUIDE.md)
- [新闻分析问题诊断](NEWS_ANALYSIS_FIX_GUIDE.md)
- [Google Custom Search API 文档](https://developers.google.com/custom-search/v1/overview)

## 🎯 总结

✅ **已完成**：
- Google Custom Search API 集成
- Streamlit Secrets 支持
- 智能优先级回退
- 详细日志记录
- 诊断工具更新

✅ **优势**：
- 官方 API，稳定可靠
- 支持中英文搜索
- 在 Streamlit Cloud 上可用
- 免费版足够日常使用

✅ **配置简单**：
1. 获取 API Key 和 CX
2. 添加到 Streamlit Secrets
3. 自动生效，无需重启

现在您的 TradingAgents 拥有了更稳定的新闻数据源！🎉

