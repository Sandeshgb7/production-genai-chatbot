
from fastapi import APIRouter, Depends
from app.schemas import ChatRequest, ChatResponse, HistoryResponse
from app.services.chat import handle_chat
from app.services.chat import get_chat_history
from app.core import create_access_token
from app.schemas import LoginRequest
from app.core import get_current_user

router = APIRouter()

@router.post("/login")
async def login(req: LoginRequest):
    token = create_access_token({"user_id": req.user_id})
    return {"access_token": token}

@router.post("/chat")
async def chat(req: ChatRequest, user_id: str = Depends(get_current_user)):
    reply = await handle_chat(user_id, req.session_id, req.message)
    return {"response": reply}

@router.get("/history", response_model=HistoryResponse)
async def history(user_id: str, session_id: str, limit: int = 20, offset: int = 0):
    data = await get_chat_history(user_id, session_id, limit, offset)
    return {"history": data}