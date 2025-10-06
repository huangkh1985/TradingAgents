#!/usr/bin/env python3
"""
Streamlit Cloud 环境设置检查脚本
用于诊断云端部署问题
"""

import os
import sys
from pathlib import Path

def check_environment():
    """检查环境配置"""
    print("=" * 60)
    print("🔍 TradingAgents-CN 环境检查")
    print("=" * 60)
    
    # 1. Python 环境
    print(f"\n✅ Python 版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # 2. 项目路径
    project_root = Path(__file__).parent
    print(f"✅ 项目路径: {project_root}")
    
    # 3. 检查关键目录
    print("\n📁 目录检查:")
    dirs_to_check = ['web', 'tradingagents', 'config', 'data']
    for dir_name in dirs_to_check:
        dir_path = project_root / dir_name
        status = "✅" if dir_path.exists() else "❌"
        print(f"  {status} {dir_name}: {dir_path.exists()}")
    
    # 4. 检查必要的包
    print("\n📦 依赖包检查:")
    packages = [
        'streamlit',
        'langchain',
        'openai',
        'pandas',
        'tradingagents'
    ]
    
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg} (缺失)")
    
    # 5. 检查环境变量/Secrets
    print("\n🔑 API 密钥检查:")
    api_keys = [
        'OPENAI_API_KEY',
        'DASHSCOPE_API_KEY',
        'GOOGLE_API_KEY',
        'TUSHARE_TOKEN'
    ]
    
    configured_keys = []
    for key in api_keys:
        value = os.getenv(key)
        if value and value != f"your-{key.lower().replace('_', '-')}":
            configured_keys.append(key)
            print(f"  ✅ {key}: 已配置")
        else:
            print(f"  ⚠️ {key}: 未配置")
    
    # 6. 检查 Streamlit Secrets
    print("\n🔐 Streamlit Secrets 检查:")
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            if st.secrets:
                print(f"  ✅ Secrets 已加载，包含 {len(st.secrets)} 个配置组")
                for section in st.secrets:
                    print(f"    - {section}")
            else:
                print("  ⚠️ Secrets 为空")
        else:
            print("  ⚠️ Secrets 不可用（可能在非 Streamlit 环境）")
    except Exception as e:
        print(f"  ⚠️ 无法检查 Secrets: {e}")
    
    # 7. 总结
    print("\n" + "=" * 60)
    print("📊 检查总结:")
    print("=" * 60)
    
    if len(configured_keys) == 0:
        print("❌ 未配置任何 API 密钥")
        print("   请在 Streamlit Cloud → Settings → Secrets 中配置")
    elif len(configured_keys) < len(api_keys):
        print(f"⚠️ 部分 API 密钥已配置 ({len(configured_keys)}/{len(api_keys)})")
        print("   建议配置所有密钥以获得完整功能")
    else:
        print("✅ 所有 API 密钥已配置")
    
    print("\n💡 提示:")
    print("  - 如果在本地运行，请创建 .env 文件配置 API 密钥")
    print("  - 如果在 Streamlit Cloud，请在 Secrets 中配置")
    print("  - 参考 .streamlit/secrets.toml.example 查看配置格式")
    print()

if __name__ == "__main__":
    check_environment()

