"""
LLM客户端模块
负责初始化和管理LLM客户端
"""

from langchain_community.chat_models import ChatOpenAI
from config import (
    OPENROUTER_API_KEY,
    MODEL_NAME,
    OPENROUTER_BASE_URL,
    LLM_TEMPERATURE
)


def init_llm_client():
    """
    初始化LLM客户端。
    
    返回:
        ChatOpenAI实例，如果初始化失败则返回None
    """
    # 检查 API Key 是否存在
    if not OPENROUTER_API_KEY:
        print("⚠️  警告：环境变量 OPENROUTER_API_KEY 未加载，将使用关键词演示结果。")
        return None
    
    try:
        # 使用 LangChain ChatOpenAI 类，通过 base_url 指定 OpenRouter 接口
        llm = ChatOpenAI(
            model=MODEL_NAME,
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENROUTER_API_KEY,
            temperature=LLM_TEMPERATURE
        )
        print(f"✅ LLM 客户端初始化成功，模型: {MODEL_NAME}")
        return llm
    except Exception as e:
        print(f"❌ LangChain客户端初始化失败: {e}，将使用关键词演示结果。")
        return None

