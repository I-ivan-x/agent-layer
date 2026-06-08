# Agent 层设计

Q1 版本采用单轮 RAG Agent：

用户请求 -> 参数校验 -> trace_id -> Retrieval Adapter -> Context Assembler -> Prompt Builder -> Mock LLM -> Answer Formatter -> JSON 响应。

## 设计边界

- 只处理单轮问答。
- 只返回普通 JSON。
- Retrieval 和 LLM 都是 Mock。
- 不接真实 HSBC 系统，不处理真实客户、员工或权限数据。

## 模块职责

- `api`：Web 路由入口。
- `service`：Agent 主流程编排。
- `retrieval`：检索接口和 Mock 检索。
- `prompt`：上下文组装和 Prompt 生成。
- `llm`：LLM 抽象和 Mock LLM。
- `formatter`：统一响应和 citations。
- `trace/logger/config/errors`：基础设施能力。

