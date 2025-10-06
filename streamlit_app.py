#!/usr/bin/env python3
"""
Streamlit Cloud 部署入口文件 - 极简测试版本
逐步排查问题
"""

import streamlit as st
import sys
from pathlib import Path

# 设置页面配置
st.set_page_config(
    page_title="TradingAgents-CN 测试",
    page_icon="📈",
    layout="wide"
)

# 显示欢迎信息
st.title("🎉 TradingAgents-CN 应用")
st.success("✅ 应用已成功启动！")

st.markdown("---")

# 显示基本信息
st.header("📊 系统信息")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Python 版本", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

with col2:
    st.metric("Streamlit", st.__version__)

with col3:
    project_root = Path(__file__).parent.absolute()
    st.metric("项目根目录", "已找到")

st.markdown("---")

# 测试状态
st.header("🔍 部署测试")

with st.expander("✅ 第一步：基础启动测试", expanded=True):
    st.success("应用成功启动并显示此页面")
    st.info("说明：Streamlit Cloud 环境配置正确")

with st.expander("📝 下一步测试计划"):
    st.markdown("""
    **逐步测试项目：**
    
    1. ✅ 基础 Streamlit 应用（当前）
    2. ⏳ 添加项目路径和导入测试
    3. ⏳ 测试日志系统
    4. ⏳ 测试认证系统
    5. ⏳ 测试完整 Web 应用
    
    **如果看到此页面，说明：**
    - Streamlit Cloud 部署成功
    - Python 环境正常
    - 包依赖安装正确
    """)

st.markdown("---")

# 登录测试区域
st.header("🔐 快速登录测试")

st.info("""
**默认测试账号：**
- 管理员：`admin` / `admin123`
- 普通用户：`user` / `user123`

等待完整功能恢复后可用。
""")

# 显示调试信息
with st.expander("🛠️ 调试信息"):
    st.code(f"""
项目根目录: {Path(__file__).parent.absolute()}
工作目录: {Path.cwd()}
Python 路径: {sys.path[:3]}
    """)

st.markdown("---")
st.caption("TradingAgents-CN v1.0 | 部署测试版本")
