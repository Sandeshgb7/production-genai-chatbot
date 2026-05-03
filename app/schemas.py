from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


class HistoryResponse(BaseModel):
    history: list

class LoginRequest(BaseModel):
    user_id: str