from fastapi import FastAPI

from agent.api.chat_routes import router as chat_router

app = FastAPI(title="agent-layer", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(chat_router, prefix="/api")

