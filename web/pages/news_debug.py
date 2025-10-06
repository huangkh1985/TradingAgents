"""
新闻数据源调试页面
用于快速诊断新闻获取问题
"""

import streamlit as st
import os
import requests
from datetime import datetime

st.set_page_config(page_title="新闻数据源调试", page_icon="🔧")

st.title("🔧 新闻数据源调试工具")
st.markdown("---")

# 1. 检查 Streamlit Secrets
st.header("1. 📋 Streamlit Secrets 检查")

if hasattr(st, 'secrets'):
    st.success("✅ Streamlit Secrets 可用")
    
    # 检查 google_search section
    st.subheader("Google Custom Search 配置")
    
    api_key = None
    cx = None
    
    if 'google_search' in st.secrets:
        st.success("✅ 找到 [google_search] section")
        api_key = st.secrets['google_search'].get('API_KEY')
        cx = st.secrets['google_search'].get('CX')
        
        if api_key:
            st.info(f"📌 API_KEY: {api_key[:20]}...{api_key[-4:]}")
        else:
            st.error("❌ API_KEY 未配置")
        
        if cx:
            st.info(f"📌 CX: {cx[:15]}...{cx[-4:]}")
        else:
            st.error("❌ CX 未配置")
    else:
        st.warning("⚠️ [google_search] section 不存在")
        
        # 检查直接配置
        api_key = st.secrets.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
        cx = st.secrets.get('GOOGLE_CUSTOM_SEARCH_CX')
        
        if api_key:
            st.info(f"ℹ️ 找到 GOOGLE_CUSTOM_SEARCH_API_KEY: {api_key[:20]}...")
        if cx:
            st.info(f"ℹ️ 找到 GOOGLE_CUSTOM_SEARCH_CX: {cx[:15]}...")
        
        if not api_key or not cx:
            st.error("❌ Google Custom Search 配置缺失")
            st.markdown("""
            ### 📝 正确的配置格式：
            
            ```toml
            [google_search]
            API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            CX = "c09a7a52c4c364088"
            ```
            """)
    
    # 检查其他配置
    st.subheader("其他 LLM 配置")
    
    llm_configs = []
    
    if 'llm' in st.secrets:
        openai_key = st.secrets['llm'].get('OPENAI_API_KEY')
        if openai_key and openai_key not in ['your_openai_api_key_here', '']:
            llm_configs.append("OpenAI")
            st.success(f"✅ OpenAI: {openai_key[:20]}...")
        
        google_key = st.secrets['llm'].get('GOOGLE_API_KEY')
        if google_key and google_key not in ['your_google_api_key_here', '']:
            llm_configs.append("Google AI")
            st.success(f"✅ Google AI: {google_key[:20]}...")
        
        deepseek_key = st.secrets['llm'].get('DEEPSEEK_API_KEY')
        if deepseek_key and deepseek_key not in ['your_deepseek_api_key_here', '']:
            llm_configs.append("DeepSeek")
            st.success(f"✅ DeepSeek: {deepseek_key[:20]}...")
    
    if llm_configs:
        st.info(f"📊 已配置的 LLM: {', '.join(llm_configs)}")
    else:
        st.warning("⚠️ 未配置其他 LLM API")
        
else:
    st.error("❌ Streamlit Secrets 不可用")

st.markdown("---")

# 2. 测试 Google Custom Search API
st.header("2. 🔍 Google Custom Search API 测试")

if api_key and cx:
    test_query = st.text_input("测试查询", value="002183 股票 新闻")
    
    if st.button("🚀 测试 API", type="primary"):
        with st.spinner("正在测试..."):
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cx,
                'q': test_query,
                'num': 3
            }
            
            try:
                start_time = datetime.now()
                response = requests.get(url, params=params, timeout=15)
                elapsed = (datetime.now() - start_time).total_seconds()
                
                st.info(f"⏱️ 请求耗时: {elapsed:.2f} 秒")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'items' in data:
                        items = data['items']
                        st.success(f"✅ API 测试成功！获取到 {len(items)} 条结果")
                        
                        st.subheader("📰 搜索结果:")
                        for i, item in enumerate(items, 1):
                            with st.expander(f"{i}. {item.get('title', 'N/A')}"):
                                st.write(f"**来源**: {item.get('displayLink', 'N/A')}")
                                st.write(f"**摘要**: {item.get('snippet', 'N/A')}")
                                st.write(f"**链接**: {item.get('link', 'N/A')}")
                    else:
                        st.warning("⚠️ API 返回成功但没有搜索结果")
                        st.json(data)
                        
                elif response.status_code == 403:
                    st.error("❌ 错误 403: API 密钥无效或 Custom Search API 未启用")
                    st.markdown("""
                    ### 解决方案：
                    1. 检查 API 密钥是否正确
                    2. 访问 [Google Cloud Console](https://console.cloud.google.com/apis/library/customsearch.googleapis.com)
                    3. 确保 Custom Search API 已启用
                    """)
                    
                elif response.status_code == 429:
                    st.error("❌ 错误 429: API 配额已用完")
                    st.info("免费版每天限制 100 次查询。请等待明天配额重置。")
                    
                else:
                    st.error(f"❌ API 返回错误: {response.status_code}")
                    st.code(response.text[:1000])
                    
            except requests.exceptions.Timeout:
                st.error("❌ 请求超时（15秒）")
                
            except Exception as e:
                st.error(f"❌ 测试失败: {type(e).__name__}: {e}")
else:
    st.warning("⚠️ Google Custom Search API 未配置，无法测试")
    st.info("请先在 Streamlit Secrets 中配置 API_KEY 和 CX")

st.markdown("---")

# 3. 测试统一新闻工具
st.header("3. 📡 统一新闻工具测试")

stock_code = st.text_input("股票代码", value="002183")

if st.button("🧪 测试新闻获取", type="primary"):
    with st.spinner("正在获取新闻..."):
        try:
            from tradingagents.tools.unified_news_tool import create_unified_news_tool
            from tradingagents.agents.utils.agent_utils import Toolkit
            
            toolkit = Toolkit()
            news_tool = create_unified_news_tool(toolkit)
            
            start_time = datetime.now()
            result = news_tool(stock_code=stock_code, max_news=10, model_info="调试测试")
            elapsed = (datetime.now() - start_time).total_seconds()
            
            st.info(f"⏱️ 获取耗时: {elapsed:.2f} 秒")
            
            if result and len(result.strip()) > 100:
                st.success(f"✅ 新闻获取成功！内容长度: {len(result)} 字符")
                
                with st.expander("📄 查看完整结果", expanded=True):
                    st.markdown(result[:2000] + "..." if len(result) > 2000 else result)
            elif result:
                st.warning(f"⚠️ 获取到部分内容: {len(result)} 字符")
                st.code(result)
            else:
                st.error("❌ 未获取到新闻数据")
                
        except Exception as e:
            st.error(f"❌ 测试失败: {type(e).__name__}: {e}")
            import traceback
            with st.expander("查看详细错误"):
                st.code(traceback.format_exc())

st.markdown("---")

# 4. AKShare 测试（如果在本地）
st.header("4. 📊 AKShare 测试")

if st.button("🧪 测试 AKShare"):
    with st.spinner("正在测试 AKShare..."):
        try:
            import akshare as ak
            
            start_time = datetime.now()
            news_df = ak.stock_news_em(symbol=stock_code.replace('.SH', '').replace('.SZ', ''))
            elapsed = (datetime.now() - start_time).total_seconds()
            
            st.info(f"⏱️ 请求耗时: {elapsed:.2f} 秒")
            
            if news_df is not None and not news_df.empty:
                st.success(f"✅ AKShare 测试成功！获取 {len(news_df)} 条新闻")
                st.dataframe(news_df.head(5))
            else:
                st.warning("⚠️ AKShare 返回空数据")
                st.info("如果在 Streamlit Cloud 上，这是正常的（地理位置限制）")
                
        except Exception as e:
            st.error(f"❌ AKShare 测试失败: {e}")
            st.info("如果在 Streamlit Cloud 上，这是正常的（AKShare 不支持境外服务器）")

st.markdown("---")

# 5. 环境信息
st.header("5. 💻 环境信息")

col1, col2 = st.columns(2)

with col1:
    st.subheader("系统信息")
    try:
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        st.info(f"主机名: {hostname}")
        st.info(f"IP地址: {ip}")
    except:
        st.warning("无法获取系统信息")

with col2:
    st.subheader("Python 包版本")
    try:
        import akshare
        st.info(f"AKShare: {akshare.__version__ if hasattr(akshare, '__version__') else '未知'}")
    except:
        st.warning("AKShare 未安装")
    
    try:
        import requests
        st.info(f"Requests: {requests.__version__}")
    except:
        pass

st.markdown("---")

# 6. 配置建议
st.header("6. 💡 配置建议")

if not api_key or not cx:
    st.error("⚠️ Google Custom Search API 未配置")
    st.markdown("""
    ### 配置步骤：
    
    1. **获取 API Key**:
       - 访问 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
       - 创建 API 密钥
    
    2. **获取 CX（搜索引擎 ID）**:
       - 访问 [Programmable Search Engine](https://programmablesearchengine.google.com/)
       - 创建搜索引擎（选择"搜索整个网络"）
       - 获取搜索引擎 ID
    
    3. **配置 Streamlit Secrets**:
       ```toml
       [google_search]
       API_KEY = "您的API密钥"
       CX = "您的搜索引擎ID"
       ```
    
    4. **重启应用**
    """)
elif not llm_configs:
    st.warning("⚠️ 建议配置至少一个 LLM API 作为备用")
    st.markdown("""
    ### 推荐配置：
    
    ```toml
    [llm]
    OPENAI_API_KEY = "sk-xxx..."
    OPENAI_API_BASE = "https://api.openai.com/v1"
    ```
    """)
else:
    st.success("✅ 配置完整！")
    st.balloons()

# 底部提示
st.markdown("---")
st.info("""
💡 **提示**: 
- 如果 Google Custom Search 配置正确但仍无法获取新闻，请检查 API 配额
- 免费版每天限制 100 次查询
- 可以配置其他 LLM API 作为备用新闻源
""")

