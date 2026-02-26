from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatMessage(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    data: dict | None = None

@router.post("/message", response_model=ChatResponse)
async def chat_message(body: ChatMessage):
    return ChatResponse(
        session_id=body.session_id,
        response="Agente em construção. Em breve respondendo suas perguntas! 🚀",
        data=None
    )