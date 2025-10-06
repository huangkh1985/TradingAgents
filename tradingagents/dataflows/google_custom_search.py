#!/usr/bin/env python3
"""
Google Custom Search API 新闻搜索
使用官方API替代网页爬虫，提供更稳定的新闻搜索服务
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class GoogleCustomSearchNews:
    """使用Google Custom Search API获取新闻"""
    
    def __init__(self):
        """初始化Google Custom Search客户端"""
        # 优先从Streamlit Secrets读取
        self.api_key = None
        self.cx = None
        
        # 1. 尝试从Streamlit Secrets读取
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                # 支持多种配置格式
                if 'google_search' in st.secrets:
                    self.api_key = st.secrets['google_search'].get('API_KEY')
                    self.cx = st.secrets['google_search'].get('CX')
                elif 'GOOGLE_CUSTOM_SEARCH_API_KEY' in st.secrets:
                    self.api_key = st.secrets.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
                    self.cx = st.secrets.get('GOOGLE_CUSTOM_SEARCH_CX')
        except:
            pass
        
        # 2. 回退到环境变量
        if not self.api_key:
            self.api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
        if not self.cx:
            self.cx = os.getenv('GOOGLE_CUSTOM_SEARCH_CX')
        
        # 日志记录配置状态
        if self.api_key and self.cx:
            logger.info(f"[Google Custom Search] 配置成功: API Key={self.api_key[:20]}..., CX={self.cx[:15]}...")
        else:
            logger.warning(f"[Google Custom Search] 未配置: API Key={'✓' if self.api_key else '✗'}, CX={'✓' if self.cx else '✗'}")
    
    def is_configured(self) -> bool:
        """检查是否已配置"""
        return bool(self.api_key and self.cx)
    
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
            新闻列表，每个新闻包含title, link, snippet, source, date
        """
        if not self.is_configured():
            logger.error("[Google Custom Search] API未配置，无法搜索")
            return []
        
        # 构建API请求URL
        url = "https://www.googleapis.com/customsearch/v1"
        
        # 转换日期格式
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            logger.error(f"[Google Custom Search] 日期格式错误: {e}")
            return []
        
        # 计算日期范围（天数）
        days_diff = (end - start).days
        if days_diff < 0:
            logger.error(f"[Google Custom Search] 结束日期早于开始日期")
            return []
        
        # 构建请求参数
        params = {
            'key': self.api_key,
            'cx': self.cx,
            'q': query,
            'num': min(max_results, 10),  # API限制：每次最多10个结果
            'sort': 'date',  # 按日期排序
        }
        
        # 添加日期限制（如果有）
        if days_diff > 0:
            params['dateRestrict'] = f'd{days_diff}'  # 最近N天
        
        try:
            logger.info(f"[Google Custom Search] 开始搜索: '{query}', 日期范围: {start_date} 至 {end_date}")
            start_time = datetime.now()
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            elapsed = (datetime.now() - start_time).total_seconds()
            data = response.json()
            
            # 检查是否有搜索结果
            if 'items' not in data:
                logger.warning(f"[Google Custom Search] 未找到搜索结果，查询: '{query}'")
                if 'error' in data:
                    error_msg = data['error'].get('message', '未知错误')
                    logger.error(f"[Google Custom Search] API错误: {error_msg}")
                # 🔍 记录完整的API响应以便调试
                logger.debug(f"[Google Custom Search] 完整API响应: {data}")
                return []
            
            items = data['items']
            logger.info(f"[Google Custom Search] 获取到 {len(items)} 条结果，耗时 {elapsed:.2f} 秒")
            logger.info(f"[Google Custom Search] 📋 结果预览: {[item.get('title', 'N/A')[:50] for item in items[:3]]}")
            
            # 解析搜索结果
            news_list = []
            for idx, item in enumerate(items):
                try:
                    # 提取新闻信息
                    news_item = {
                        'title': item.get('title', '无标题'),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', '无摘要'),
                        'source': item.get('displayLink', '未知来源'),
                        'date': ''
                    }
                    
                    # 尝试提取发布日期
                    pagemap = item.get('pagemap', {})
                    metatags = pagemap.get('metatags', [{}])
                    if metatags:
                        # 尝试多种日期字段
                        date_fields = ['article:published_time', 'publishdate', 'datePublished', 'date']
                        for field in date_fields:
                            if field in metatags[0]:
                                news_item['date'] = metatags[0][field]
                                break
                    
                    news_list.append(news_item)
                    
                    if idx < 3:  # 只记录前3条的详细信息
                        logger.debug(f"[Google Custom Search] 新闻{idx+1}: {news_item['title'][:50]}...")
                        
                except Exception as e:
                    logger.warning(f"[Google Custom Search] 解析第{idx+1}条结果失败: {e}")
                    continue
            
            return news_list
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error("[Google Custom Search] ❌ API配额已用完（每天限100次免费查询）")
            elif e.response.status_code == 403:
                logger.error("[Google Custom Search] ❌ API密钥无效或未启用Custom Search API")
            else:
                logger.error(f"[Google Custom Search] ❌ HTTP错误 {e.response.status_code}: {e}")
            return []
            
        except requests.exceptions.Timeout:
            logger.error("[Google Custom Search] ❌ 请求超时（15秒）")
            return []
            
        except Exception as e:
            logger.error(f"[Google Custom Search] ❌ 搜索失败: {type(e).__name__}: {e}")
            return []


def get_google_custom_search_news(
    query: str, 
    curr_date: str, 
    look_back_days: int = 7
) -> str:
    """
    使用Google Custom Search API获取新闻（对外接口）
    
    Args:
        query: 搜索查询
        curr_date: 当前日期 (YYYY-MM-DD)
        look_back_days: 回溯天数
        
    Returns:
        格式化的新闻字符串
    """
    searcher = GoogleCustomSearchNews()
    
    if not searcher.is_configured():
        logger.warning("[Google Custom Search] API未配置，跳过")
        return ""
    
    # 计算日期范围
    try:
        end_date = datetime.strptime(curr_date, "%Y-%m-%d")
        start_date = end_date - timedelta(days=look_back_days)
    except ValueError as e:
        logger.error(f"[Google Custom Search] 日期格式错误: {e}")
        return ""
    
    # 搜索新闻
    news_list = searcher.search_news(
        query=query,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=curr_date,
        max_results=10
    )
    
    if not news_list:
        logger.warning(f"[Google Custom Search] 未获取到新闻数据")
        return ""
    
    # 格式化输出
    news_str = ""
    for idx, news in enumerate(news_list):
        news_str += f"### {news['title']}\n\n"
        news_str += f"📅 {news['date'] or '日期未知'} | 📰 来源: {news['source']}\n\n"
        news_str += f"{news['snippet']}\n\n"
        news_str += f"🔗 [{news['link']}]({news['link']})\n\n"
        news_str += "---\n\n"
    
    header = f"## 📰 Google Custom Search 新闻\n\n"
    header += f"**搜索查询**: {query}\n\n"
    header += f"**时间范围**: {start_date.strftime('%Y-%m-%d')} 至 {curr_date}\n\n"
    header += f"**新闻数量**: {len(news_list)} 条\n\n"
    header += "---\n\n"
    
    final_result = header + news_str
    
    # 🔍 记录返回结果的长度和内容预览
    logger.info(f"[Google Custom Search] 📊 格式化完成，总长度: {len(final_result)} 字符")
    logger.info(f"[Google Custom Search] 📋 格式化内容预览 (前300字符): {final_result[:300]}")
    
    return final_result


# 测试函数
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 测试
    result = get_google_custom_search_news(
        query="002183 股票 新闻 财报",
        curr_date="2025-01-06",
        look_back_days=7
    )
    
    if result:
        print("✅ 测试成功！")
        print(result[:500] + "..." if len(result) > 500 else result)
    else:
        print("❌ 测试失败：未获取到新闻数据")
        print("\n请检查：")
        print("1. 是否配置了 GOOGLE_CUSTOM_SEARCH_API_KEY")
        print("2. 是否配置了 GOOGLE_CUSTOM_SEARCH_CX")
        print("3. API密钥是否有效")
        print("4. 是否启用了Custom Search API")

