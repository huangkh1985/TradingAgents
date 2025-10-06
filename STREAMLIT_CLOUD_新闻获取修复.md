# Streamlit Cloud 新闻获取问题修复指南

## 📋 问题描述

在 Streamlit Cloud 上运行时，即使 Google Custom Search API 配置正确且调试工具显示能获取数据，但在实际新闻分析中仍然显示"无法获取新闻"。

### 症状
- ✅ 调试工具显示：API 配置正确
- ✅ 调试工具显示：能获取到 3 条搜索结果
- ❌ 实际分析时：无法获取新闻

## 🔍 根本原因

问题出在**长度阈值判断过于严格**：

```python
# 原始代码 (tradingagents/tools/unified_news_tool.py)
if result and len(result.strip()) > 100:  # 要求至少 100 字符
    return self._format_news_result(result, "Google Custom Search API", model_info)
```

**问题分析**：
1. Google Custom Search API 返回的原始数据可能较短
2. 当搜索结果只有 1-3 条且摘要较短时，格式化后的内容可能少于 100 字符
3. 即使 API 正常工作，返回的有效数据也会被过滤掉
4. 导致系统认为"获取失败"，继续尝试其他数据源

## ✅ 修复方案

### 1. 降低长度阈值

将长度阈值从 **100 字符降低到 50 字符**，避免有效数据被过滤：

```python
# 修复后的代码
if result and len(result.strip()) > 50:  # 从 100 降低到 50
    logger.info(f"[统一新闻工具] ✅ Google Custom Search API获取成功: {len(result)} 字符")
    return self._format_news_result(result, "Google Custom Search API", model_info)
```

### 2. 添加详细调试日志

增强日志记录，帮助快速定位问题：

```python
# 🔍 添加详细的调试日志
logger.info(f"[统一新闻工具] 📊 Google Custom Search API 返回结果长度: {len(result) if result else 0} 字符")
if result:
    logger.info(f"[统一新闻工具] 📋 返回内容预览 (前300字符): {result[:300]}")

# 🔧 修复：降低长度阈值，避免有效数据被过滤
if result and len(result.strip()) > 50:  # 从 100 降低到 50
    logger.info(f"[统一新闻工具] ✅ Google Custom Search API获取成功: {len(result)} 字符")
    return self._format_news_result(result, "Google Custom Search API", model_info)
elif result:
    logger.warning(f"[统一新闻工具] ⚠️ Google Custom Search API返回内容过短: {len(result)} 字符，内容: {result}")
else:
    logger.warning(f"[统一新闻工具] ⚠️ Google Custom Search API返回空内容")
```

### 3. 增强错误跟踪

添加异常堆栈跟踪，便于调试：

```python
except Exception as e:
    logger.warning(f"[统一新闻工具] Google Custom Search API失败: {e}")
    import traceback
    logger.debug(f"[统一新闻工具] 详细错误: {traceback.format_exc()}")
```

## 📝 修复的文件

### 1. `tradingagents/tools/unified_news_tool.py`
- ✅ A股新闻获取：降低长度阈值 + 增强日志
- ✅ 港股新闻获取：降低长度阈值 + 增强日志  
- ✅ 美股新闻获取：降低长度阈值 + 增强日志

### 2. `tradingagents/dataflows/google_custom_search.py`
- ✅ 添加搜索结果预览日志
- ✅ 添加格式化内容长度和预览日志
- ✅ 记录完整 API 响应以便调试

## 🧪 验证步骤

### 1. 在调试工具中测试

访问侧边栏的"🔧 新闻调试工具"：

```
📋 配置检查
✅ 找到配置 (google_search section)
API_KEY: AIzaSyC3EGWzyuk73Cpx...xQ48
CX: 127878b1d43794d...

✅ API 正常！获取到 3 条结果
- 怡亚通(002183) 股价、新闻、报价和图表- 富途牛牛
- 怡亚通(002183)股票股价, 市值, 实时行情, 走势图, 财报- Moomoo
```

### 2. 在实际分析中测试

1. 在主页面输入股票代码（如 `002183`）
2. 选择"📰 新闻事件分析"
3. 点击"🚀 开始分析"
4. 查看日志输出

### 3. 检查日志输出

正常情况下应该看到：

```
[统一新闻工具] 尝试Google Custom Search API...
[Google Custom Search] 获取到 3 条结果，耗时 1.23 秒
[Google Custom Search] 📋 结果预览: ['怡亚通(002183) 股价、新闻、报价和图表...', ...]
[Google Custom Search] 📊 格式化完成，总长度: 687 字符
[统一新闻工具] 📊 Google Custom Search API 返回结果长度: 687 字符
[统一新闻工具] ✅ Google Custom Search API获取成功: 687 字符
```

## 🔧 Streamlit Cloud 部署注意事项

### 确保 Secrets 配置正确

在 Streamlit Cloud 的 Settings → Secrets 中配置：

```toml
[google_search]
API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CX = "您的搜索引擎ID"

[llm]
OPENAI_API_KEY = "sk-xxx..."
OPENAI_API_BASE = "https://api.openai.com/v1"
```

### 重启应用

修复代码后，需要在 Streamlit Cloud 上：
1. 提交并推送代码到 GitHub
2. Streamlit Cloud 会自动检测更新
3. 等待应用重新部署（约 1-2 分钟）

## 📊 预期效果

修复后的效果：

| 修复前 | 修复后 |
|--------|--------|
| ❌ 无法获取新闻数据 | ✅ 成功获取新闻 |
| 🔍 长度阈值: 100 字符 | 🔍 长度阈值: 50 字符 |
| 📝 日志信息少 | 📝 详细的调试日志 |
| ⚠️ 有效数据被过滤 | ✅ 保留所有有效数据 |

## 💡 附加建议

### 1. 监控 API 配额

Google Custom Search API 免费版：
- 每天 **100 次查询**
- 超出后返回 429 错误

建议配置其他备用新闻源：
- OpenAI 全球新闻（需配置 OPENAI_API_KEY）
- Google 新闻网页爬虫（可能不稳定）

### 2. 日志级别设置

在本地开发时，可以设置更详细的日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

在生产环境（Streamlit Cloud）建议使用 INFO 级别。

### 3. 定期检查

建议定期检查：
- ✅ Google Custom Search API 配额使用情况
- ✅ API 密钥是否有效
- ✅ 搜索引擎 ID 是否正确
- ✅ 备用新闻源是否可用

## 🎯 总结

本次修复解决了 Streamlit Cloud 上新闻获取失败的核心问题：

1. **根本原因**：长度阈值过严，导致有效数据被过滤
2. **修复方案**：降低阈值 + 增强日志
3. **影响范围**：A股、港股、美股的所有 Google Custom Search API 调用
4. **预期效果**：能够正常获取和显示新闻数据

---

**修复完成时间**: 2025-10-06  
**版本**: v0.1.x  
**影响模块**: 新闻分析模块

