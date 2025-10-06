"""
API密钥检查工具
"""

import os

def _get_secret(key, section=None):
    """
    获取密钥，支持多种来源：
    1. Streamlit Secrets (优先，用于 Streamlit Cloud)
    2. 环境变量 (用于本地开发)
    """
    try:
        import streamlit as st
        # 尝试从 Streamlit Secrets 读取
        if section:
            return st.secrets.get(section, {}).get(key)
        else:
            # 尝试从所有 section 中查找
            for sec in st.secrets:
                if isinstance(st.secrets[sec], dict) and key in st.secrets[sec]:
                    return st.secrets[sec][key]
            return None
    except:
        # 如果不在 Streamlit 环境或 Secrets 不可用，使用环境变量
        return os.getenv(key)

def check_api_keys():
    """检查所有必要的API密钥是否已配置"""

    # 检查各个API密钥（优先从 Streamlit Secrets 读取）
    dashscope_key = _get_secret("DASHSCOPE_API_KEY", "llm") or os.getenv("DASHSCOPE_API_KEY")
    finnhub_key = _get_secret("FINNHUB_API_KEY", "data_sources") or os.getenv("FINNHUB_API_KEY")
    openai_key = _get_secret("OPENAI_API_KEY", "llm") or os.getenv("OPENAI_API_KEY")
    anthropic_key = _get_secret("ANTHROPIC_API_KEY", "llm") or os.getenv("ANTHROPIC_API_KEY")
    google_key = _get_secret("GOOGLE_API_KEY", "llm") or os.getenv("GOOGLE_API_KEY")
    qianfan_key = _get_secret("QIANFAN_ACCESS_KEY", "llm") or os.getenv("QIANFAN_API_KEY")

    
    # 构建详细状态
    details = {
        "OPENAI_API_KEY": {
            "configured": bool(openai_key),
            "display": f"{openai_key[:12]}..." if openai_key else "未配置",
            "required": False,
            "description": "OpenAI API密钥",
            "category": "llm"
        },
        "DASHSCOPE_API_KEY": {
            "configured": bool(dashscope_key),
            "display": f"{dashscope_key[:12]}..." if dashscope_key else "未配置",
            "required": False,
            "description": "阿里百炼API密钥",
            "category": "llm"
        },
        "ANTHROPIC_API_KEY": {
            "configured": bool(anthropic_key),
            "display": f"{anthropic_key[:12]}..." if anthropic_key else "未配置",
            "required": False,
            "description": "Anthropic API密钥",
            "category": "llm"
        },
        "GOOGLE_API_KEY": {
            "configured": bool(google_key),
            "display": f"{google_key[:12]}..." if google_key else "未配置",
            "required": False,
            "description": "Google AI API密钥",
            "category": "llm"
        },
        "QIANFAN_ACCESS_KEY": {
            "configured": bool(qianfan_key),
            "display": f"{qianfan_key[:16]}..." if qianfan_key else "未配置",
            "required": False,
            "description": "文心一言（千帆）API Key（OpenAI兼容），一般以 bce-v3/ 开头",
            "category": "llm"
        },
        "FINNHUB_API_KEY": {
            "configured": bool(finnhub_key),
            "display": f"{finnhub_key[:12]}..." if finnhub_key else "未配置",
            "required": False,
            "description": "金融数据API密钥（可选，可使用免费的AKShare）",
            "category": "data"
        },
        # QIANFAN_SECRET_KEY 不再用于OpenAI兼容路径，仅保留给脚本示例使用
        # "QIANFAN_SECRET_KEY": {
        #     "configured": bool(qianfan_sk),
        #     "display": f"{qianfan_sk[:12]}..." if qianfan_sk else "未配置",
        #     "required": False,
        #     "description": "文心一言（千帆）Secret Key (仅脚本示例)"
        # },
    }
    
    # 检查至少配置了一个 LLM API 密钥
    llm_keys = [key for key, info in details.items() if info.get("category") == "llm"]
    llm_configured = any(details[key]["configured"] for key in llm_keys)
    
    # 检查必需的API密钥（现在只要求至少一个 LLM）
    required_keys = [key for key, info in details.items() if info["required"]]
    missing_required = [key for key in required_keys if not details[key]["configured"]]
    
    # 如果没有配置任何 LLM，标记为不完整
    all_configured = llm_configured and len(missing_required) == 0
    
    return {
        "all_configured": all_configured,
        "required_configured": len(missing_required) == 0,
        "missing_required": missing_required,
        "llm_configured": llm_configured,
        "details": details,
        "summary": {
            "total": len(details),
            "configured": sum(1 for info in details.values() if info["configured"]),
            "required": len(required_keys),
            "required_configured": len(required_keys) - len(missing_required),
            "llm_configured": llm_configured
        }
    }

def get_api_key_status_message():
    """获取API密钥状态消息"""
    
    status = check_api_keys()
    
    if not status["llm_configured"]:
        return "❌ 至少需要配置一个 LLM API 密钥（OpenAI、DashScope、Anthropic 等）"
    elif status["all_configured"]:
        return "✅ API 密钥配置完成，可以开始使用"
    elif status["required_configured"]:
        return "✅ 基础配置完成，可选配置未完成"
    else:
        missing = ", ".join(status["missing_required"])
        return f"❌ 缺少必需的API密钥: {missing}"

def validate_api_key_format(key_type, api_key):
    """验证API密钥格式"""
    
    if not api_key:
        return False, "API密钥不能为空"
    
    # 基本长度检查
    if len(api_key) < 10:
        return False, "API密钥长度过短"
    
    # 特定格式检查
    if key_type == "DASHSCOPE_API_KEY":
        if not api_key.startswith("sk-"):
            return False, "阿里百炼API密钥应以'sk-'开头"
    elif key_type == "OPENAI_API_KEY":
        if not api_key.startswith("sk-"):
            return False, "OpenAI API密钥应以'sk-'开头"
    elif key_type == "QIANFAN_API_KEY":
        if not api_key.startswith("bce-v3/"):
            return False, "千帆 API Key（OpenAI兼容）应以 'bce-v3/' 开头"
    
    return True, "API密钥格式正确"

def test_api_connection(key_type, api_key):
    """测试API连接（简单验证）"""
    
    # 这里可以添加实际的API连接测试
    # 为了简化，现在只做格式验证
    
    is_valid, message = validate_api_key_format(key_type, api_key)
    
    if not is_valid:
        return False, message
    
    # 可以在这里添加实际的API调用测试
    # 例如：调用一个简单的API端点验证密钥有效性
    
    return True, "API密钥验证通过"
