class AgentError(Exception):
    pass


class RetrievalError(AgentError):
    pass


class LLMError(AgentError):
    pass

