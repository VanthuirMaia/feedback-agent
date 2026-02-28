from fastapi import APIRouter, HTTPException
from app.core.store import store
from pydantic import BaseModel
from app.agent.graph import agent
import uuid

router = APIRouter()


class ChatMessage(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    data: dict | None = None


@router.post("/message", response_model=ChatResponse)
async def chat_message(body: ChatMessage):
    session_id = body.session_id or str(uuid.uuid4())

    initial_state = {
        "messages": [{"role": "user", "content": body.message}],
        "session_id": session_id,
        "feedbacks_df": store.get(),
        "query_intent": "",
        "filters": {},
        "sql_query": "",
        "result": {},
        "response": "",
    }

    try:
        final_state = await agent.ainvoke(initial_state)
        return ChatResponse(
            session_id=session_id,
            response=final_state["response"],
            data=final_state.get("result"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))