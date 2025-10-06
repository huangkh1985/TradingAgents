#!/usr/bin/env python3
"""
新闻获取修复验证脚本
用于测试 Google Custom Search API 是否能正常获取新闻
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_google_custom_search():
    """测试 Google Custom Search API"""
    print("=" * 60)
    print("🧪 测试 Google Custom Search API")
    print("=" * 60)
    
    try:
        from tradingagents.dataflows.google_custom_search import get_google_custom_search_news
        from datetime import datetime
        
        # 测试参数
        stock_code = "002183"
        curr_date = datetime.now().strftime("%Y-%m-%d")
        query = f"{stock_code} 股票 新闻 财报 业绩"
        
        print(f"\n📋 测试参数:")
        print(f"   股票代码: {stock_code}")
        print(f"   查询关键词: {query}")
        print(f"   当前日期: {curr_date}")
        print(f"   回溯天数: 7")
        
        print(f"\n🚀 开始测试...")
        result = get_google_custom_search_news(query, curr_date, look_back_days=7)
        
        print(f"\n📊 测试结果:")
        if result:
            print(f"   ✅ 获取成功！")
            print(f"   📝 内容长度: {len(result)} 字符")
            print(f"   📋 内容预览 (前 500 字符):")
            print(f"   {'-' * 60}")
            print(f"   {result[:500]}")
            print(f"   {'-' * 60}")
            
            # 检查长度阈值
            if len(result) > 50:
                print(f"   ✅ 长度检查通过 (> 50 字符)")
            else:
                print(f"   ⚠️ 长度过短 ({len(result)} 字符)")
        else:
            print(f"   ❌ 未获取到数据")
            print(f"\n💡 可能的原因:")
            print(f"   1. Google Custom Search API 未配置")
            print(f"   2. API 配额已用完（每天 100 次）")
            print(f"   3. API 密钥无效")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        print(f"\n详细错误:")
        print(traceback.format_exc())


def test_unified_news_tool():
    """测试统一新闻工具"""
    print("\n" + "=" * 60)
    print("🧪 测试统一新闻工具")
    print("=" * 60)
    
    try:
        from tradingagents.tools.unified_news_tool import create_unified_news_tool
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        # 创建工具包和新闻工具
        toolkit = Toolkit()
        news_tool = create_unified_news_tool(toolkit)
        
        # 测试参数
        stock_code = "002183"
        
        print(f"\n📋 测试参数:")
        print(f"   股票代码: {stock_code}")
        print(f"   最大新闻数: 10")
        print(f"   模型信息: 测试模式")
        
        print(f"\n🚀 开始测试...")
        result = news_tool(stock_code=stock_code, max_news=10, model_info="测试模式")
        
        print(f"\n📊 测试结果:")
        if result:
            print(f"   ✅ 获取成功！")
            print(f"   📝 内容长度: {len(result)} 字符")
            print(f"   📋 内容预览 (前 500 字符):")
            print(f"   {'-' * 60}")
            print(f"   {result[:500]}")
            print(f"   {'-' * 60}")
            
            # 检查是否包含新闻数据源标识
            if "Google Custom Search API" in result:
                print(f"   ✅ 使用 Google Custom Search API")
            elif "东方财富" in result:
                print(f"   ✅ 使用东方财富实时新闻")
            elif "Google新闻" in result:
                print(f"   ✅ 使用 Google 新闻（网页爬虫）")
            else:
                print(f"   ℹ️ 使用其他新闻源")
        else:
            print(f"   ❌ 未获取到数据")
            print(f"\n💡 检查日志输出以了解详情")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        print(f"\n详细错误:")
        print(traceback.format_exc())


def check_configuration():
    """检查配置"""
    print("=" * 60)
    print("🔍 检查配置")
    print("=" * 60)
    
    # 检查环境变量
    print(f"\n📋 环境变量:")
    api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
    cx = os.getenv('GOOGLE_CUSTOM_SEARCH_CX')
    
    if api_key:
        print(f"   ✅ GOOGLE_CUSTOM_SEARCH_API_KEY: {api_key[:20]}...")
    else:
        print(f"   ❌ GOOGLE_CUSTOM_SEARCH_API_KEY: 未配置")
    
    if cx:
        print(f"   ✅ GOOGLE_CUSTOM_SEARCH_CX: {cx[:15]}...")
    else:
        print(f"   ❌ GOOGLE_CUSTOM_SEARCH_CX: 未配置")
    
    # 检查 Streamlit Secrets
    print(f"\n📋 Streamlit Secrets:")
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            if 'google_search' in st.secrets:
                api_key_st = st.secrets['google_search'].get('API_KEY')
                cx_st = st.secrets['google_search'].get('CX')
                
                if api_key_st:
                    print(f"   ✅ [google_search] API_KEY: {api_key_st[:20]}...")
                if cx_st:
                    print(f"   ✅ [google_search] CX: {cx_st[:15]}...")
            else:
                print(f"   ℹ️ [google_search] section 不存在")
        else:
            print(f"   ℹ️ Streamlit Secrets 不可用（非 Streamlit 环境）")
    except ImportError:
        print(f"   ℹ️ Streamlit 未安装（非 Streamlit 环境）")


if __name__ == "__main__":
    print("\n🔧 新闻获取修复验证工具\n")
    
    # 1. 检查配置
    check_configuration()
    
    # 2. 测试 Google Custom Search API
    test_google_custom_search()
    
    # 3. 测试统一新闻工具
    test_unified_news_tool()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    
    print(f"\n💡 提示:")
    print(f"   - 如果测试失败，请检查 Google Custom Search API 配置")
    print(f"   - 确保 API_KEY 和 CX 已正确配置")
    print(f"   - 检查 API 配额是否用完（每天 100 次免费）")
    print(f"   - 查看详细日志了解具体错误原因")
    print()

