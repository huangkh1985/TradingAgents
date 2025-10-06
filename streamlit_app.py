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

# 切换到 web 目录，确保相对导入正确
os.chdir(web_dir)

# 导入并运行主应用（直接导入，不使用 runpy）
# 这样 Streamlit 可以正确处理
import runpy
runpy.run_path(str(web_dir / "app.py"), run_name="__main__")

