from uuid import uuid4


def generate_trace_id() -> str:
    return f"trace-{uuid4().hex[:8]}"

