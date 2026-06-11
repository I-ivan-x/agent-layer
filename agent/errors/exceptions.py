"""
自定义异常模块
"""

class AgentError(Exception):
    """Agent 基础异常"""
    pass


class RetrievalError(AgentError):
    """检索异常"""
    pass


class LLMError(AgentError):
    """LLM 调用异常"""
    pass


class InvalidQueryError(AgentError):
    """无效查询异常"""
    pass


class NoRelevantContextError(AgentError):
    """无相关内容异常"""
    pass


class ConfigError(AgentError):
    """配置错误"""
    pass