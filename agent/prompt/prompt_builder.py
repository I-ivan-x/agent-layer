from agent.prompt.templates import SYSTEM_ROLE, ANSWER_RULES


class PromptBuilder:
    def build(self, query: str, context: str) -> str:
        return f"""{SYSTEM_ROLE}

用户问题：
{query}

检索上下文：
{context}

严格约束：
{ANSWER_RULES}
"""

