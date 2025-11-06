# 日志挖掘项目 (Log Mining Project)

本项目旨在演示如何利用**开源大语言模型 (LLM)** 的自然语言推理能力，通过 **API 调用** 对系统日志进行自动化分析和异常诊断。

## 技术栈

* **核心技术**: **OpenRouter API**（统一接口）
* **核心模型**: **MiniMax M2 (free)** (开源 MoE 模型，优化于 Agentic 工作流和推理)
* **框架**: **Python**, **LangChain** (用于简洁地封装 API 调用和管理消息格式)
* **依赖管理**: **python-dotenv** (用于安全管理 API Key)
* **任务**: 日志异常诊断与原因分析

## 如何运行（API 调用方式）

本项目通过调用 OpenRouter 平台上的高性能开源 LLM 来实现实际的日志分析。

### 1. 环境准备

请使用 pip 安装所需的依赖库：

```bash
pip install -r requirements.txt