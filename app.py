from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import run_agent

app = FastAPI(title="TravelBuddy API", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User input message")


class ChatResponse(BaseModel):
    reply: str
    trace_id: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        user_message = payload.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="message must not be empty")

        result = run_agent(user_message)
        final_message = result["messages"][-1].content if result.get("messages") else ""
        trace_id = result.get("trace_id", "-")
        return ChatResponse(reply=final_message, trace_id=trace_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=500, detail="Hệ thống đang bị lỗi..."
        )
