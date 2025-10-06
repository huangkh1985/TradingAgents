"""
新闻获取快速测试工具
可以直接在主页面中调用
"""

import streamlit as st
import requests
from datetime import datetime

def show_news_debug():
    """显示新闻调试信息"""
    
    with st.expander("🔧 新闻获取诊断工具", expanded=False):
        st.markdown("### 📋 配置检查")
        
        # 检查配置
        api_key = None
        cx = None
        config_source = None
        
        if hasattr(st, 'secrets'):
            # 方式1: google_search section
            if 'google_search' in st.secrets:
                api_key = st.secrets['google_search'].get('API_KEY')
                cx = st.secrets['google_search'].get('CX')
                config_source = "google_search section"
            
            # 方式2: 直接配置
            if not api_key:
                api_key = st.secrets.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
                cx = st.secrets.get('GOOGLE_CUSTOM_SEARCH_CX')
                config_source = "直接配置"
        
        if api_key and cx:
            st.success(f"✅ 找到配置 ({config_source})")
            st.code(f"""
API_KEY: {api_key[:20]}...{api_key[-4:] if len(api_key) > 24 else ''}
CX: {cx[:15]}...{cx[-4:] if len(cx) > 19 else ''}
            """)
            
            # 测试API
            if st.button("🧪 测试 Google Custom Search API"):
                with st.spinner("测试中..."):
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
                            if 'items' in data:
                                st.success(f"✅ API 正常！获取到 {len(data['items'])} 条结果")
                                for item in data['items'][:2]:
                                    st.write(f"- {item.get('title', 'N/A')}")
                            else:
                                st.warning("⚠️ API 正常但无搜索结果")
                        elif response.status_code == 403:
                            st.error("❌ 403错误: API未启用或密钥无效")
                            st.info("解决: 访问 https://console.cloud.google.com/apis/library/customsearch.googleapis.com 启用API")
                        elif response.status_code == 429:
                            st.error("❌ 429错误: 配额已用完")
                            st.info("免费版每天100次，请明天再试")
                        else:
                            st.error(f"❌ 错误 {response.status_code}: {response.text[:200]}")
                    
                    except Exception as e:
                        st.error(f"❌ 测试失败: {e}")
        else:
            st.error("❌ Google Custom Search API 未配置")
            st.markdown("""
            ### 📝 请在 Streamlit Secrets 中添加：
            
            ```toml
            [google_search]
            API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            CX = "您的搜索引擎ID"
            ```
            
            或使用测试配置：
            
            ```toml
            [google_search]
            API_KEY = "AIzaSyDdGgiiUegHEwWRqIhBoh-hEfQDWOeLres"
            CX = "c09a7a52c4c364088"
            ```
            """)
        
        # 显示其他配置
        st.markdown("### 📊 其他 LLM 配置")
        
        other_llms = []
        if hasattr(st, 'secrets') and 'llm' in st.secrets:
            if st.secrets['llm'].get('OPENAI_API_KEY'):
                other_llms.append("OpenAI")
            if st.secrets['llm'].get('GOOGLE_API_KEY'):
                other_llms.append("Google AI")
            if st.secrets['llm'].get('DEEPSEEK_API_KEY'):
                other_llms.append("DeepSeek")
        
        if other_llms:
            st.info(f"已配置: {', '.join(other_llms)}")
        else:
            st.warning("未配置其他 LLM API")


def quick_test_news(stock_code="002183"):
    """快速测试新闻获取"""
    
    st.markdown("### 🧪 快速测试新闻获取")
    
    if st.button("测试获取新闻", type="primary"):
        with st.spinner(f"正在获取 {stock_code} 的新闻..."):
            try:
                from tradingagents.tools.unified_news_tool import create_unified_news_tool
                from tradingagents.agents.utils.agent_utils import Toolkit
                
                toolkit = Toolkit()
                news_tool = create_unified_news_tool(toolkit)
                
                result = news_tool(stock_code=stock_code, max_news=10, model_info="快速测试")
                
                if result and len(result.strip()) > 100:
                    st.success("✅ 获取成功！")
                    with st.expander("查看新闻内容"):
                        st.markdown(result[:1000] + "..." if len(result) > 1000 else result)
                else:
                    st.error("❌ 未获取到新闻")
                    st.info("可能的原因：")
                    st.write("1. Google Custom Search API 未配置")
                    st.write("2. 所有新闻源都不可用")
                    st.write("3. API 配额已用完")
                    
            except Exception as e:
                st.error(f"❌ 错误: {e}")
                import traceback
                with st.expander("详细错误"):
                    st.code(traceback.format_exc())

