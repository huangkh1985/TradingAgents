"""
Streamlit Secrets 和环境变量统一读取辅助工具
支持 Streamlit Cloud 和本地开发环境
"""

import os
from typing import Optional

def get_api_key(key_name: str, section: Optional[str] = None) -> Optional[str]:
    """
    从多个来源获取 API 密钥（按优先级）：
    1. Streamlit Secrets (优先，用于 Streamlit Cloud)
    2. 环境变量 (用于本地开发)
    
    Args:
        key_name: API 密钥名称，如 "OPENAI_API_KEY"
        section: Streamlit Secrets 中的 section 名称，如 "llm" 或 "data_sources"
    
    Returns:
        API 密钥字符串，如果未找到则返回 None
    
    Examples:
        >>> get_api_key("OPENAI_API_KEY", "llm")
        'sk-xxxx'
        
        >>> get_api_key("FINNHUB_API_KEY", "data_sources")
        'xxxx'
    """
    # 1. 尝试从 Streamlit Secrets 读取
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            # 如果指定了 section，直接从该 section 读取
            if section and section in st.secrets:
                if key_name in st.secrets[section]:
                    value = st.secrets[section][key_name]
                    if value:  # 确保不是空字符串
                        return value
            
            # 尝试从所有 section 中查找
            for sec in st.secrets:
                if isinstance(st.secrets[sec], dict) and key_name in st.secrets[sec]:
                    value = st.secrets[sec][key_name]
                    if value:  # 确保不是空字符串
                        return value
            
            # 也尝试从顶层读取（兼容旧格式）
            if key_name in st.secrets:
                value = st.secrets[key_name]
                if value:
                    return value
    except:
        pass  # 不在 Streamlit 环境或 Secrets 不可用，继续尝试环境变量
    
    # 2. 从环境变量读取
    value = os.getenv(key_name)
    if value:
        return value
    
    # 3. 未找到
    return None


def get_api_base_url(provider: str) -> Optional[str]:
    """
    获取 LLM 提供商的 API Base URL
    
    Args:
        provider: LLM 提供商名称，如 "openai", "dashscope"
    
    Returns:
        API Base URL 字符串，如果未配置则返回 None
    """
    # 定义各提供商的 Base URL 环境变量名
    url_key_map = {
        "openai": "OPENAI_API_BASE",
        "dashscope": "DASHSCOPE_BASE_URL",
        "deepseek": "DEEPSEEK_BASE_URL",
        "anthropic": "ANTHROPIC_BASE_URL",
    }
    
    key_name = url_key_map.get(provider.lower())
    if not key_name:
        return None
    
    return get_api_key(key_name, "llm")


# 便捷函数：直接获取常用 API 密钥
def get_openai_api_key() -> Optional[str]:
    """获取 OpenAI API 密钥"""
    return get_api_key("OPENAI_API_KEY", "llm")


def get_openai_api_base() -> Optional[str]:
    """获取 OpenAI API Base URL"""
    return get_api_key("OPENAI_API_BASE", "llm")


def get_dashscope_api_key() -> Optional[str]:
    """获取 DashScope API 密钥"""
    return get_api_key("DASHSCOPE_API_KEY", "llm")


def get_anthropic_api_key() -> Optional[str]:
    """获取 Anthropic API 密钥"""
    return get_api_key("ANTHROPIC_API_KEY", "llm")


def get_google_api_key() -> Optional[str]:
    """获取 Google API 密钥"""
    return get_api_key("GOOGLE_API_KEY", "llm")


def get_deepseek_api_key() -> Optional[str]:
    """获取 DeepSeek API 密钥"""
    return get_api_key("DEEPSEEK_API_KEY", "llm")


def get_finnhub_api_key() -> Optional[str]:
    """获取 Finnhub API 密钥"""
    return get_api_key("FINNHUB_API_KEY", "data_sources")


def get_tushare_token() -> Optional[str]:
    """获取 Tushare Token"""
    return get_api_key("TUSHARE_TOKEN", "data_sources")


