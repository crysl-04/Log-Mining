"""
统计报告模块
负责生成统计报告和结果分析
"""

from collections import Counter
from diagnosis import parse_diagnosis_result
from config import SEVERITY_ORDER, SEVERITY_MARKERS


def generate_statistics_report(results: list) -> dict:
    """
    根据诊断结果生成统计报告。
    
    参数:
        results: 诊断结果列表，每个元素包含 {"log": "...", "diagnosis": "..."}
    
    返回:
        统计信息字典，包含：
        - total_logs: 总日志数
        - severity_distribution: 严重程度分布
        - summary: 文本摘要列表
        - parsed_results: 解析后的结构化结果
    """
    # 统计各严重程度的数量
    severity_counter = Counter()
    total_logs = len(results)
    
    # 解析每条日志的严重程度
    parsed_results = []
    for item in results:
        parsed = parse_diagnosis_result(item.get("diagnosis", ""))
        severity = parsed["severity"]
        severity_counter[severity] += 1
        
        # 保存解析后的结果
        parsed_item = {
            "log": item.get("log", ""),
            "severity": severity,
            "diagnosis": parsed["diagnosis"]
        }
        parsed_results.append(parsed_item)
    
    # 计算占比
    statistics = {
        "total_logs": total_logs,
        "severity_distribution": {},
        "summary": []
    }
    
    # 统计各严重程度的数量和占比
    for severity in SEVERITY_ORDER:
        count = severity_counter.get(severity, 0)
        if count > 0:
            percentage = (count / total_logs * 100) if total_logs > 0 else 0
            statistics["severity_distribution"][severity] = {
                "count": count,
                "percentage": round(percentage, 2)
            }
    
    # 生成摘要文本
    summary_lines = _generate_summary_text(statistics, severity_counter)
    statistics["summary"] = summary_lines
    statistics["parsed_results"] = parsed_results
    
    return statistics


def _generate_summary_text(statistics: dict, severity_counter: Counter) -> list:
    """
    生成统计摘要文本。
    
    参数:
        statistics: 统计信息字典
        severity_counter: 严重程度计数器
    
    返回:
        摘要文本行列表
    """
    total_logs = statistics["total_logs"]
    
    summary_lines = [
        f"📊 日志分析统计报告",
        f"{'='*50}",
        f"总日志条数: {total_logs}",
        f"",
        f"严重程度分布:",
    ]
    
    # 添加各严重程度的统计信息
    for severity in SEVERITY_ORDER:
        if severity in statistics["severity_distribution"]:
            info = statistics["severity_distribution"][severity]
            marker = SEVERITY_MARKERS.get(severity, "⚪")
            
            summary_lines.append(
                f"  {marker} {severity}: {info['count']} 条 ({info['percentage']}%)"
            )
    
    # 添加关键信息
    critical_count = severity_counter.get("严重", 0)
    error_count = severity_counter.get("错误", 0)
    
    summary_lines.append("")
    summary_lines.append("关键信息:")
    if critical_count > 0:
        summary_lines.append(f"  ⚠️  发现 {critical_count} 条严重错误，需要立即处理！")
    if error_count > 0:
        summary_lines.append(f"  ⚠️  发现 {error_count} 条错误，建议尽快检查。")
    if critical_count == 0 and error_count == 0:
        summary_lines.append(f"  ✅ 未发现严重错误或错误，系统运行正常。")
    
    return summary_lines


def print_statistics_report(statistics: dict):
    """
    在控制台打印统计报告。
    
    参数:
        statistics: 统计信息字典
    """
    print("\n" + "\n".join(statistics["summary"]) + "\n")

