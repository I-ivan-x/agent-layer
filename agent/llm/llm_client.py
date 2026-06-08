from agent.llm.base import BaseLLM


class LLMClient(BaseLLM):
    def generate(self, prompt: str) -> str:
        # TODO: Q2 后按配置接入真实 LLM Client。此处不读取真实 API Key，也不调用真实 API。
        raise NotImplementedError("Real LLM client is not enabled in Q1.")

