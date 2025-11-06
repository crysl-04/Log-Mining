"""
日志挖掘主程序
负责协调各个模块，完成日志分析的完整流程
"""

import json
import os
from config import (
    LOG_FILE_PATH,
    OUTPUT_DIR,
    OUTPUT_DIAGNOSIS_RESULTS,
    OUTPUT_STATISTICS_REPORT,
    OUTPUT_STRUCTURED_RESULTS
)
from llm_client import init_llm_client
from diagnosis import diagnose_log_entry
from statistics import generate_statistics_report, print_statistics_report


def process_log_file(log_file_path: str = None):
    """
    处理日志文件，进行诊断和统计分析。
    
    参数:
        log_file_path: 日志文件路径，如果为None则使用配置文件中的默认路径
    """
    # 使用默认路径或指定路径
    file_path = log_file_path or LOG_FILE_PATH
    
    print("--- 日志挖掘：基于LangChain+OpenRouter的日志诊断系统启动 ---")
    
    # 初始化LLM客户端
    llm_client = init_llm_client()
    
    # 读取日志文件
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        
        print(f"\n开始分析 {len(log_lines)} 条日志...")
        
        # 逐条诊断日志
        for i, line in enumerate(log_lines):
            if line.strip():
                diagnosis = diagnose_log_entry(llm_client, line)
                results.append({"log": line.strip(), "diagnosis": diagnosis})
                
                print(f"[{i+1}] Log: {line.strip()[:60]}...")
                print(f"    Diagnosis: {diagnosis}")
    
    except FileNotFoundError:
        print(f"❌ 错误：未找到日志文件 {file_path}。请确保已创建该文件。")
        return
    
    # 确保输出目录存在
    _ensure_output_dir()
    
    # 生成输出文件的完整路径
    diagnosis_path = os.path.join(OUTPUT_DIR, OUTPUT_DIAGNOSIS_RESULTS)
    statistics_path = os.path.join(OUTPUT_DIR, OUTPUT_STATISTICS_REPORT)
    structured_path = os.path.join(OUTPUT_DIR, OUTPUT_STRUCTURED_RESULTS)
    
    # 保存原始诊断结果
    _save_results(results, diagnosis_path)
    
    # 生成统计报告
    print("\n正在生成统计报告...")
    statistics = generate_statistics_report(results)
    
    # 打印统计报告
    print_statistics_report(statistics)
    
    # 保存统计报告
    _save_results(statistics, statistics_path)
    
    # 保存结构化结果
    _save_results(statistics["parsed_results"], structured_path)
    
    # 输出完成信息
    print(f"--- 日志挖掘分析完成 ---")
    print(f"📁 所有结果已保存到目录: {OUTPUT_DIR}/")
    print(f"📄 详细诊断结果: {diagnosis_path}")
    print(f"📊 统计报告: {statistics_path}")
    print(f"📋 结构化结果: {structured_path}")


def _ensure_output_dir():
    """
    确保输出目录存在，如果不存在则创建。
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 已创建输出目录: {OUTPUT_DIR}")


def _save_results(data: dict or list, file_path: str):
    """
    保存结果到JSON文件。
    
    参数:
        data: 要保存的数据（字典或列表）
        file_path: 保存路径（可以是相对路径或绝对路径）
    """
    # 确保目录存在
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


def main():
    """主函数入口"""
    process_log_file()


if __name__ == "__main__":
    main()
