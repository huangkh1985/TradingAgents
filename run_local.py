"""
本地运行 Streamlit 应用的简化脚本
自动处理环境配置和路径问题
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("="*80)
    print("🚀 启动 TradingAgents-CN Web 应用")
    print("="*80)
    print()
    
    # 确保在项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 检查必要文件
    web_app = project_root / "web" / "app.py"
    if not web_app.exists():
        print("❌ 错误：找不到 web/app.py")
        print("   请确保在项目根目录运行此脚本")
        return
    
    print(f"✅ 项目目录: {project_root}")
    print(f"✅ 应用文件: {web_app}")
    print()
    print("🌐 启动 Streamlit 服务器...")
    print("   浏览器将自动打开 http://localhost:8501")
    print()
    print("💡 提示：按 Ctrl+C 停止服务器")
    print("="*80)
    print()
    
    try:
        # 直接运行 web/app.py（推荐方式）
        # 切换到 web 目录以确保相对导入正确
        os.chdir(project_root / "web")
        
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  服务器已停止")
    except FileNotFoundError:
        print("\n❌ 错误：streamlit 未安装")
        print("   请运行: pip install streamlit")
    except Exception as e:
        print(f"\n❌ 错误: {e}")

if __name__ == "__main__":
    main()

