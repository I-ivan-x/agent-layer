# agent-layer

`agent-layer` 是 AI 智能问答项目 Q1 阶段的 Agent 层仓库，用于实现简化版单轮 RAG Agent。当前版本只使用 Mock Retrieval 和 Mock LLM 打通 Web-Agent 最小闭环。

## Q1 范围

- FastAPI 服务入口
- `GET /health`
- `POST /api/chat`
- ChatRequest / ChatResponse / Citation 接口契约
- Mock Retrieval
- Context Assembler
- Prompt Builder V1
- Mock LLM
- Answer Formatter
- trace_id、基础 logger、状态码和 pytest

## 不做内容

- 不实现复杂多步 Agent
- 不连接真实 HSBC 系统
- 不读取真实密钥
- 不接真实客户、员工、权限数据
- 不调用真实 LLM
- 不调用真实检索工具
- 不连接 Milvus、BM25 或 embedding API
- SSE / fetch stream 仅预留，不强制实现真实流式输出

## 目录结构

```text
agent-layer/
├── app.py
├── agent/
│   ├── api/
│   ├── service/
│   ├── formatter/
│   ├── schemas/
│   ├── prompt/
│   ├── llm/
│   ├── retrieval/
│   ├── trace/
│   ├── logger/
│   ├── config/
│   ├── errors/
│   └── streaming/
├── mock/
├── tests/
├── docs/
└── scripts/
```

## 运行方式

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## 测试方式

```bash
pytest
```

## API 示例

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"项目 Q1 阶段需要完成哪些功能？\",\"stream\":false}"
```

成功响应示例：

```json
{
  "trace_id": "trace-xxxxxxxx",
  "status": "success",
  "answer": "Q1 阶段需要完成简化版单轮 RAG Agent，包括 /api/chat、Mock Retrieval、Prompt Builder、Mock LLM 和 Answer Formatter 等最小闭环能力。[1]",
  "message": "",
  "citations": []
}
```

## Mock 说明

- `agent/retrieval/mock_retrieval.py` 默认返回 3 条模拟文档块。
- `agent/llm/mock_llm.py` 返回带 `[1]` 引用编号的模拟答案。
- `mock/` 目录提供请求、检索结果和答案样例。
- `RetrievalAdapter` 和 `LLMClient` 只保留真实接入位置，不触发真实调用。

## 分工建议

成员 A：Agent 业务主流程负责人，也就是 xdj

- `agent/api/`
- `agent/service/`
- `agent/prompt/`
- `agent/llm/`
- `agent/formatter/`
- `agent/schemas/chat.py`
- `docs/interface_contract.md`

成员 B：Agent 基础设施负责人，也就是 lhf

- `agent/retrieval/`
- `agent/logger/`
- `agent/trace/`
- `agent/config/`
- `agent/errors/`
- `tests/`
- `agent/schemas/retrieval.py`

共同负责：

- `agent/schemas/common.py`
- Web 联调
- Bug 修复
- Demo 问题集验证
- `docs/integration_record.md`

## Git 协作建议

- `main`：稳定版本
- `dev`：日常开发版本
- `feature/agent-core`：xdj 开发 Agent 主流程
- `feature/agent-infra`：lhf 开发基础设施和检索适配
- `feature/integration`：第 3-4 周联调分支

## 下一步接真实检索

1. 在 `agent/retrieval/retrieval_adapter.py` 中增加真实 Tool Layer 客户端。
2. 保持 `BaseRetriever.retrieve()` 返回 `list[RetrievalResult]`。
3. 在配置中增加 mock / real 模式切换。
4. 增加真实检索异常到 `retrieval_error` 的映射测试。

## 下一步接真实 LLM

1. 在 `agent/llm/llm_client.py` 中实现真实 LLM Client。
2. 从安全配置或部署环境读取密钥，禁止写入仓库。
3. 保持 `BaseLLM.generate(prompt: str) -> str` 接口稳定。
4. 增加超时、限流、异常到 `llm_error` 的映射测试。

