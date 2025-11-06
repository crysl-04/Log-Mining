import os
import json
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ==============================================================================
# 1. API 配置与加载
# ==============================================================================
load_dotenv() 

# 从环境变量中读取密钥
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") 

#MODEL_NAME = "openai/gpt-5" 
MODEL_NAME = "minimax/minimax-m2:free"
# MODEL_NAME = "mistralai/mistral-7b-instruct" # 替代选择：轻量级/低费用

LOG_FILE_PATH = "sample.log"
SYSTEM_PROMPT = """你是一位专业的系统日志分析师。你的任务是根据提供的日志列表，判断每条日志是否包含严重错误或异常。
请严格按照 JSON 数组格式输出结果，不要输出任何其他内容。
JSON 格式要求：
[
    {
        "index": <日志行号>, 
        "log": <原始日志内容>,
        "severity": <判断等级：如 '正常', '警告', '错误', '严重'>,
        "diagnosis": <简短的诊断结论和潜在原因>
    },
    ...
]
"""

# ==============================================================================
# 2. 初始化 LLM 客户端
# ==============================================================================
# 检查 API Key 是否存在
if not OPENROUTER_API_KEY:
    llm = None
    print(" 警告：环境变量 OPENROUTER_API_KEY 未加载，将使用关键词演示结果。")
else:
    try:
        # 使用 LangChain ChatOpenAI 类，通过 base_url 指定 OpenRouter 接口
        llm = ChatOpenAI(
            model=MODEL_NAME,
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            temperature=0  # 设置为0以获得更稳定的诊断结果
        )
        print(f" LLM 客户端初始化成功，模型: {MODEL_NAME}")
    except Exception as e:
        llm = None
        print(f" LangChain客户端初始化失败: {e}，将使用关键词演示结果。")


# ==============================================================================
# 3. 日志处理函数：利用 LangChain 调用 LLM
# ==============================================================================
def diagnose_log_entry_langchain(log_line: str) -> str:
    """
    使用 LangChain LLM 实例诊断单条日志。
    """
    user_log = f"请诊断这条日志：\n{log_line.strip()}"
    
    if llm:
        try:
            # 构造 Messages 列表
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_log)
            ]
            
            # ** 实际 API 调用 **
            response = llm.invoke(messages)
            diagnosis_text = response.content.strip()
            
            return f"实际API诊断结果 (LangChain): {diagnosis_text}"
            
        except Exception as e:
            return f"API 调用失败。错误：{e} (请检查 OpenRouter 账户和费用)"
    else:
        # ** 退回到关键词演示模式 **
        if "ERROR" in log_line or "Fatal" in log_line:
            return "诊断结论：严重异常！ 潜在原因：根据关键词判断为致命错误，需要立即检查。 (演示结果)"
        elif "WARN" in log_line:
            return "诊断结论：轻微警告。 潜在原因：可能是资源不足或超时，建议优化配置。 (演示结果)"
        else:
            return "诊断结论：日志正常。 (演示结果)"


# ==============================================================================
# 4. 主程序 (保持不变)
# ==============================================================================
def main():
    print("--- 日志挖掘：基于LangChain+OpenRouter的日志诊断系统启动 ---")
    results = []
    
    try:
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        
        print(f"\n开始分析 {len(log_lines)} 条日志...")
        for i, line in enumerate(log_lines):
            if line.strip():
                diagnosis = diagnose_log_entry_langchain(line) # 调用新的函数
                results.append({"log": line.strip(), "diagnosis": diagnosis})
                
                print(f"[{i+1}] Log: {line.strip()[:60]}...")
                print(f"    Diagnosis: {diagnosis}")

    except FileNotFoundError:
        print(f" 错误：未找到日志文件 {LOG_FILE_PATH}。请确保已创建该文件。")
        return
    
    with open("diagnosis_results.json", 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)
    
    print("\n--- 日志挖掘分析完成。详细结果已保存到 diagnosis_results.json ---")

if __name__ == "__main__":
    main()