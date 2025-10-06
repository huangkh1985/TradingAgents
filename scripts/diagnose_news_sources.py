#!/usr/bin/env python3
"""
新闻数据源诊断脚本
快速检测新闻获取功能的可用性
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_akshare():
    """检查 AKShare 连接"""
    print_section("1. 检查 AKShare（东方财富新闻）")
    
    try:
        import akshare as ak
        print("✅ AKShare 模块已安装")
        print(f"   版本: {ak.__version__ if hasattr(ak, '__version__') else '未知'}")
        
        # 测试获取新闻
        try:
            print("\n🔍 测试获取股票 002183 的新闻...")
            start_time = datetime.now()
            news_df = ak.stock_news_em(symbol="002183")
            elapsed = (datetime.now() - start_time).total_seconds()
            
            if news_df is not None and not news_df.empty:
                print(f"✅ 成功获取 {len(news_df)} 条新闻，耗时 {elapsed:.2f} 秒")
                print(f"\n📰 最新新闻示例:")
                for idx, row in news_df.head(3).iterrows():
                    title = row.get('标题', row.get('新闻标题', '无标题'))
                    time = row.get('发布时间', '未知时间')
                    print(f"   {idx+1}. {title} ({time})")
                return True
            else:
                print(f"⚠️  API 调用成功但未返回新闻数据，耗时 {elapsed:.2f} 秒")
                return False
                
        except Exception as e:
            print(f"❌ AKShare API 调用失败: {e}")
            print(f"   错误类型: {type(e).__name__}")
            return False
            
    except ImportError as e:
        print(f"❌ AKShare 未安装: {e}")
        print("\n💡 安装方法:")
        print("   pip install akshare --upgrade")
        return False

def check_openai_api():
    """检查 OpenAI API"""
    print_section("2. 检查 OpenAI API")
    
    api_key = os.getenv('OPENAI_API_KEY')
    api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ OPENAI_API_KEY 未配置")
        print("\n💡 配置方法:")
        print("   export OPENAI_API_KEY=sk-xxx...")
        print("   或在 .env 文件中设置")
        print("   或在 Streamlit Secrets 中配置")
        return False
    
    print(f"✅ OPENAI_API_KEY 已配置: {api_key[:20]}...")
    print(f"   API Base: {api_base}")
    
    # 测试连接
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=api_base)
        
        print("\n🔍 测试 API 连接...")
        start_time = datetime.now()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ OpenAI API 连接成功，耗时 {elapsed:.2f} 秒")
        print(f"   模型: {response.model}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API 连接失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        return False

def check_google_api():
    """检查 Google AI API"""
    print_section("3. 检查 Google AI API")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY 未配置")
        print("\n💡 配置方法:")
        print("   export GOOGLE_API_KEY=AIza...")
        print("   或在 .env 文件中设置")
        return False
    
    print(f"✅ GOOGLE_API_KEY 已配置: {api_key[:20]}...")
    
    # 测试连接
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        print("\n🔍 测试 API 连接...")
        start_time = datetime.now()
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello", 
                                         generation_config={"max_output_tokens": 5})
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ Google AI API 连接成功，耗时 {elapsed:.2f} 秒")
        return True
        
    except Exception as e:
        print(f"❌ Google AI API 连接失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        return False

def check_deepseek_api():
    """检查 DeepSeek API"""
    print_section("4. 检查 DeepSeek API")
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    api_base = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    
    if not api_key:
        print("❌ DEEPSEEK_API_KEY 未配置")
        return False
    
    print(f"✅ DEEPSEEK_API_KEY 已配置: {api_key[:20]}...")
    print(f"   API Base: {api_base}")
    
    # 测试连接
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=api_base)
        
        print("\n🔍 测试 API 连接...")
        start_time = datetime.now()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ DeepSeek API 连接成功，耗时 {elapsed:.2f} 秒")
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek API 连接失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        return False

def check_google_custom_search():
    """检查 Google Custom Search API"""
    print_section("5. 检查 Google Custom Search API")
    
    api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
    cx = os.getenv('GOOGLE_CUSTOM_SEARCH_CX')
    
    # 尝试从Streamlit Secrets读取
    if not api_key or not cx:
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                if 'google_search' in st.secrets:
                    api_key = st.secrets['google_search'].get('API_KEY')
                    cx = st.secrets['google_search'].get('CX')
                else:
                    api_key = st.secrets.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
                    cx = st.secrets.get('GOOGLE_CUSTOM_SEARCH_CX')
        except:
            pass
    
    if not api_key or not cx:
        print("❌ Google Custom Search API 未配置")
        print("\n💡 配置方法:")
        print("   方式1 - 环境变量:")
        print("     export GOOGLE_CUSTOM_SEARCH_API_KEY=xxx")
        print("     export GOOGLE_CUSTOM_SEARCH_CX=xxx")
        print("\n   方式2 - Streamlit Secrets:")
        print("     [google_search]")
        print("     API_KEY = \"xxx\"")
        print("     CX = \"xxx\"")
        return False
    
    print(f"✅ API Key 已配置: {api_key[:20]}...")
    print(f"✅ CX 已配置: {cx[:15]}...")
    
    # 测试搜索
    try:
        import requests
        
        print("\n🔍 测试搜索 '002183 股票 新闻'...")
        start_time = datetime.now()
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cx,
            'q': '002183 股票 新闻',
            'num': 3
        }
        
        response = requests.get(url, params=params, timeout=10)
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            print(f"✅ Google Custom Search API 连接成功，获取到 {len(items)} 条结果，耗时 {elapsed:.2f} 秒")
            if items:
                print(f"\n📰 结果示例:")
                for i, item in enumerate(items[:2], 1):
                    print(f"   {i}. {item.get('title', 'N/A')[:60]}...")
            return True
        elif response.status_code == 403:
            print(f"❌ API密钥无效或未启用Custom Search API")
            print(f"   请访问: https://console.cloud.google.com/apis/library/customsearch.googleapis.com")
            return False
        elif response.status_code == 429:
            print(f"❌ API配额已用完（免费版每天100次）")
            return False
        else:
            print(f"❌ Google Custom Search API 返回错误: {response.status_code}")
            print(f"   {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Google Custom Search API 测试失败: {e}")
        return False

def check_finnhub_api():
    """检查 FinnHub API"""
    print_section("6. 检查 FinnHub API（美股新闻）")
    
    api_key = os.getenv('FINNHUB_API_KEY')
    
    if not api_key:
        print("❌ FINNHUB_API_KEY 未配置")
        print("\n💡 FinnHub 主要用于美股新闻，对 A股可选")
        return False
    
    print(f"✅ FINNHUB_API_KEY 已配置: {api_key[:10]}...")
    
    # 测试连接
    try:
        import requests
        
        print("\n🔍 测试获取 AAPL 的新闻...")
        start_time = datetime.now()
        url = f"https://finnhub.io/api/v1/company-news"
        params = {
            'symbol': 'AAPL',
            'from': '2024-01-01',
            'to': '2024-12-31',
            'token': api_key
        }
        response = requests.get(url, params=params, timeout=10)
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if response.status_code == 200:
            news = response.json()
            print(f"✅ FinnHub API 连接成功，获取到 {len(news)} 条新闻，耗时 {elapsed:.2f} 秒")
            return True
        else:
            print(f"❌ FinnHub API 返回错误: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FinnHub API 连接失败: {e}")
        return False

def check_unified_news_tool():
    """检查统一新闻工具"""
    print_section("7. 检查统一新闻工具集成")
    
    try:
        from tradingagents.tools.unified_news_tool import create_unified_news_tool
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        print("✅ 统一新闻工具模块导入成功")
        
        toolkit = Toolkit()
        news_tool = create_unified_news_tool(toolkit)
        
        print("\n🔍 测试获取股票 002183 的新闻（A股）...")
        start_time = datetime.now()
        result = news_tool(stock_code="002183", max_news=5, model_info="测试")
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if result and "❌" not in result[:50]:
            print(f"✅ 统一新闻工具测试成功，耗时 {elapsed:.2f} 秒")
            print(f"\n📰 返回结果预览:")
            print(result[:500] + "..." if len(result) > 500 else result)
            return True
        else:
            print(f"❌ 统一新闻工具返回失败:")
            print(result[:300])
            return False
            
    except Exception as e:
        print(f"❌ 统一新闻工具测试失败: {e}")
        import traceback
        print(f"\n详细错误:")
        print(traceback.format_exc())
        return False

def generate_recommendations(results):
    """生成改进建议"""
    print_section("诊断总结与建议")
    
    available_sources = sum(results.values())
    total_sources = len(results)
    
    print(f"\n📊 可用新闻源: {available_sources}/{total_sources}")
    print(f"\n详细状态:")
    for source, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {source}")
    
    print(f"\n\n{'='*60}")
    if available_sources == 0:
        print("⚠️  警告: 没有可用的新闻数据源！")
        print("\n建议:")
        print("1. 本地开发: 安装 AKShare")
        print("   pip install akshare --upgrade")
        print("\n2. Streamlit Cloud: 配置至少一个 API 密钥")
        print("   - OPENAI_API_KEY (推荐)")
        print("   - GOOGLE_API_KEY (有免费额度)")
        print("   - DEEPSEEK_API_KEY (便宜)")
        
    elif available_sources < 2:
        print("⚠️  注意: 只有 1 个新闻源可用")
        print("\n建议: 配置额外的新闻源作为备份")
        
    else:
        print("✅ 新闻数据获取功能正常！")
        print(f"\n您已配置 {available_sources} 个新闻源，系统会自动选择最佳来源。")
    
    print(f"{'='*60}\n")

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     TradingAgents 新闻数据源诊断工具                     ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 检查环境变量
    print("🔍 当前环境变量:")
    env_vars = ['OPENAI_API_KEY', 'GOOGLE_API_KEY', 'DEEPSEEK_API_KEY', 
                'FINNHUB_API_KEY', 'DASHSCOPE_API_KEY']
    for var in env_vars:
        value = os.getenv(var)
        if value and value not in ["your_openai_api_key_here", "your_api_key_here"]:
            print(f"   ✅ {var}: {value[:20]}...")
        else:
            print(f"   ❌ {var}: 未配置")
    
    # 执行检查
    results = {
        "AKShare (东方财富)": check_akshare(),
        "OpenAI API": check_openai_api(),
        "Google AI API": check_google_api(),
        "DeepSeek API": check_deepseek_api(),
        "Google Custom Search API": check_google_custom_search(),
        "FinnHub API": check_finnhub_api(),
        "统一新闻工具": check_unified_news_tool()
    }
    
    # 生成建议
    generate_recommendations(results)

if __name__ == "__main__":
    main()

