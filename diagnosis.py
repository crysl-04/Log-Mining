"""
日志诊断模块
负责日志的诊断和结果解析
"""

import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from config import SYSTEM_PROMPT


def diagnose_log_entry(llm_client, log_line: str) -> str:
    """
    使用 LLM 客户端诊断单条日志。
    
    参数:
        llm_client: LLM客户端实例（ChatOpenAI）
        log_line: 日志行内容
    
    返回:
        诊断结果字符串
    """
    user_log = f"请诊断这条日志：\n{log_line.strip()}"
    
    if llm_client:
        try:
            # 构造 Messages 列表
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_log)
            ]
            
            # 实际 API 调用
            response = llm_client.invoke(messages)
            diagnosis_text = response.content.strip()
            
            return f"实际API诊断结果 (LangChain): {diagnosis_text}"
            
        except Exception as e:
            return f"API 调用失败。错误：{e} (请检查 OpenRouter 账户和费用)"
    else:
        # 退回到关键词演示模式
        return _fallback_keyword_diagnosis(log_line)


def _fallback_keyword_diagnosis(log_line: str) -> str:
    """
    当LLM不可用时，使用关键词进行简单的诊断（演示模式）。
    
    参数:
        log_line: 日志行内容
    
    返回:
        诊断结果字符串
    """
    if "ERROR" in log_line or "Fatal" in log_line:
        return "诊断结论：严重异常！ 潜在原因：根据关键词判断为致命错误，需要立即检查。 (演示结果)"
    elif "WARN" in log_line:
        return "诊断结论：轻微警告。 潜在原因：可能是资源不足或超时，建议优化配置。 (演示结果)"
    else:
        return "诊断结论：日志正常。 (演示结果)"


def parse_diagnosis_result(diagnosis_text: str) -> dict:
    """
    从诊断结果字符串中解析出严重程度和诊断信息。
    
    参数:
        diagnosis_text: 诊断结果字符串
    
    返回:
        包含严重程度和诊断信息的字典
        格式: {"severity": "严重", "diagnosis": "诊断内容"}
    """
    try:
        # 尝试从字符串中提取JSON部分
        # 处理可能包含 ```json 标记的情况
        json_match = re.search(r'\[.*?\]', diagnosis_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            parsed_data = json.loads(json_str)
            if isinstance(parsed_data, list) and len(parsed_data) > 0:
                item = parsed_data[0]
                return {
                    "severity": item.get("severity", "未知"),
                    "diagnosis": item.get("diagnosis", "")
                }
    except Exception as e:
        # 如果解析失败，尝试从演示结果中提取
        pass
    
    # 从文本中提取严重程度（用于演示模式或解析失败的情况）
    if "严重异常" in diagnosis_text or "严重" in diagnosis_text:
        return {"severity": "严重", "diagnosis": diagnosis_text}
    elif "警告" in diagnosis_text:
        return {"severity": "警告", "diagnosis": diagnosis_text}
    elif "正常" in diagnosis_text:
        return {"severity": "正常", "diagnosis": diagnosis_text}
    elif "错误" in diagnosis_text:
        return {"severity": "错误", "diagnosis": diagnosis_text}
    
    return {"severity": "未知", "diagnosis": diagnosis_text}

