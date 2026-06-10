# API Contract

## POST /api/chat

Current stage: Week 1 Mock JSON chain.

The endpoint runs the minimal Agent Core flow:

```text
request validation -> ChatService -> mock retrieval -> PromptBuilder V1 -> MockLLM -> AnswerFormatter -> JSON response
```

`stream` is reserved for future SSE or fetch streaming support. In Week 1, requests with `stream: true` still return normal JSON.

## Request

```json
{
  "query": "项目 Q1 阶段需要完成哪些功能？",
  "session_id": "local-session-001",
  "top_k": 5,
  "filters": {},
  "stream": false
}
```

Fields:

- `query`: Required user question. After trimming whitespace, it must not be empty.
- `session_id`: Optional session identifier reserved for Web integration.
- `top_k`: Optional retrieval count. Default is `5`.
- `filters`: Optional retrieval filters. Default is `{}`.
- `stream`: Optional streaming flag. Default is `false`; Week 1 ignores it and returns JSON.

## Success Response

```json
{
  "trace_id": "trace-xxxxxxxx",
  "status": "success",
  "answer": "根据当前检索上下文，Q1 阶段主要需要打通用户提问、检索、Prompt 组装、答案生成和引用展示的基础链路。[1]",
  "message": "",
  "citations": [
    {
      "citation_id": 1,
      "title": "Agent 层 Q1 范围",
      "source_url": "https://example.local/docs/agent-q1-plan",
      "doc_id": "agent-q1-plan",
      "chunk_id": "chunk-001",
      "score": 0.96,
      "snippet": "Q1 只实现简化版单轮 RAG Agent，使用 Mock Retrieval 和 Mock LLM 打通最小闭环。"
    }
  ]
}
```

## Error Response

```json
{
  "trace_id": "trace-xxxxxxxx",
  "status": "invalid_query",
  "answer": "",
  "message": "请输入有效问题。",
  "citations": []
}
```

## Citations

- `citation_id`: Citation number starting from `1`.
- `title`: Source chunk title.
- `source_url`: Optional source URL.
- `doc_id`: Source document ID.
- `chunk_id`: Source chunk ID.
- `score`: Retrieval score.
- `snippet`: Short excerpt from `chunk_text` for Web display.

## Supported Status

- `success`
- `invalid_query`
- `retrieval_error`
- `llm_error`

## Not Implemented In Week 1

- Real database
- Real vector retrieval
- Real LLM
- SSE streaming
- ACL permission filtering

## Interfaces To Confirm With Member B

- Whether retrieval will expose `retrieval.search(query, top_k, filters)` or keep `retrieve(...)`.
- Standard retrieval chunk fields.
- Whether the `trace_id` function is fixed as `generate_trace_id()`.
- Final home of the status enum.
- Final ownership of `ChatRequest` and `ChatResponse` schemas.
