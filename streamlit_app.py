#!/usr/bin/env python3
"""
Streamlit Cloud 部署入口文件
此文件是 Streamlit Cloud 默认查找的入口点

使用方法：
- 本地测试: streamlit run streamlit_app.py
- Streamlit Cloud: 自动使用此文件作为入口
"""

import sys
import os
from pathlib import Path

# 确保项目根目录和 web 目录都在 Python 路径中
project_root = Path(__file__).parent.absolute()
web_dir = project_root / "web"

# 添加到 Python 路径（必须在导入前完成）
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(web_dir))

# 切换到项目根目录
os.chdir(project_root)

# 直接导入 web.app 模块，让 Streamlit 执行它
# 这种方式与 Streamlit Cloud 兼容
import importlib.util
spec = importlib.util.spec_from_file_location("app", web_dir / "app.py")
app_module = importlib.util.module_from_spec(spec)
sys.modules["app"] = app_module
spec.loader.exec_module(app_module)
