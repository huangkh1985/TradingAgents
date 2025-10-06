#!/usr/bin/env python3
"""
Streamlit Cloud 部署入口文件
TradingAgents-CN 股票分析平台
"""

import streamlit as st
import sys
import os
from pathlib import Path

# 设置页面配置 - 必须在最开始
st.set_page_config(
    page_title="TradingAgents-CN 股票分析平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# 添加项目根目录和 web 目录到 Python 路径
project_root = Path(__file__).parent.absolute()
web_dir = project_root / "web"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(web_dir))

def check_environment():
    """检查运行环境并显示状态"""
    env_info = {
        "Python版本": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Streamlit": st.__version__,
        "项目路径": str(project_root),
        "是否云端": bool(os.getenv('STREAMLIT_CLOUD', False))
    }
    return env_info

def load_environment():
    """加载环境变量"""
    try:
        from dotenv import load_dotenv
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=True)
            return True
        else:
            # 云端环境使用 secrets
            return False
    except ImportError:
        return False

def setup_secrets():
    """设置环境变量从 Streamlit secrets"""
    try:
        # 检查是否有 secrets 配置
        if hasattr(st, 'secrets') and st.secrets:
            # 从 secrets 设置环境变量
            for section in st.secrets:
                if isinstance(st.secrets[section], dict):
                    for key, value in st.secrets[section].items():
                        os.environ[key] = str(value)
            return True
        return False
    except Exception as e:
        st.warning(f"读取 secrets 配置时出错: {e}")
        return False

def check_dependencies():
    """检查必要的依赖"""
    missing_deps = []
    required_modules = [
        'tradingagents',
        'langchain',
        'openai',
        'pandas'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_deps.append(module)
    
    return missing_deps

def show_error_page(error_msg, details=None):
    """显示错误页面"""
    st.error(f"❌ {error_msg}")
    
    if details:
        with st.expander("🔍 详细信息"):
            st.code(details)
    
    st.markdown("---")
    st.info("""
    ### 📝 故障排除建议：
    
    1. **检查依赖安装**: 确保所有必要的 Python 包已安装
    2. **检查 API 密钥**: 在 Streamlit Cloud Secrets 中配置 API 密钥
    3. **查看日志**: 检查应用日志获取更多错误信息
    4. **联系支持**: 如果问题持续，请查看项目文档
    """)

def main():
    """主入口函数"""
    
    # 1. 加载环境变量
    has_env = load_environment()
    has_secrets = setup_secrets()
    
    # 显示环境状态（仅调试模式）
    if os.getenv('DEBUG_MODE') == 'true':
        env_info = check_environment()
        with st.expander("🔧 环境信息（调试模式）"):
            st.json(env_info)
            st.write(f"环境变量加载: {'✅' if has_env else '❌'}")
            st.write(f"Secrets 加载: {'✅' if has_secrets else '❌'}")
    
    # 2. 检查依赖
    missing_deps = check_dependencies()
    if missing_deps:
        show_error_page(
            "缺少必要的依赖包",
            f"缺少的包: {', '.join(missing_deps)}\n\n请运行: pip install {' '.join(missing_deps)}"
        )
        return
    
    # 3. 尝试导入并运行完整应用
    try:
        # 导入 web 应用的主函数
        from web.app import main as web_main, initialize_session_state, check_frontend_auth_cache
        
        # 运行完整应用
        web_main()
        
    except ImportError as e:
        # 如果导入失败，显示详细错误和降级方案
        error_details = f"导入错误: {str(e)}\n\nPython路径:\n" + "\n".join(sys.path)
        
        show_error_page("无法加载应用模块", error_details)
        
        # 显示基础功能降级方案
        st.markdown("---")
        st.warning("⚠️ 使用降级模式运行基础功能")
        
        st.header("📊 TradingAgents-CN 股票分析平台")
        st.info("""
        **完整功能暂时不可用，但您可以：**
        
        1. 检查 API 配置
        2. 查看系统状态
        3. 等待系统恢复
        
        **如需完整功能，请确保：**
        - 所有依赖包已正确安装
        - 项目文件结构完整
        - API 密钥已配置
        """)
        
        # 显示系统信息
        with st.expander("🔍 系统信息"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Python 版本", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
                st.metric("Streamlit 版本", st.__version__)
            with col2:
                st.metric("项目路径", "已找到" if project_root.exists() else "未找到")
                st.metric("Web 目录", "存在" if web_dir.exists() else "不存在")
        
    except Exception as e:
        # 捕获其他运行时错误
        import traceback
        error_details = f"运行时错误:\n{str(e)}\n\n堆栈跟踪:\n{traceback.format_exc()}"
        show_error_page("应用运行错误", error_details)

if __name__ == "__main__":
    main()
