from app.services.memory import get_history, save_message
from app.services.llm import generate_response
import uuid
from app.db import ChatMessage, AsyncSessionLocal
from datetime import datetime
from sqlalchemy import select
from app.db import get_session
#.venv\Scripts\Activate.ps1     
from app.agent import graph

async def handle_chat(user_id: str, session_id: str, user_input: str):
    history = await get_history(user_id, session_id)

    messages = history + [{"role": "user", "content": user_input}]

    # LangGraph execution
    result = await graph.ainvoke({"messages": messages})

    response = result["messages"][-1]["content"] 

    # save memory
    await save_message(user_id, session_id, {"role": "user", "content": user_input})
    await save_message(user_id, session_id, {"role": "assistant", "content": response})

    return response

async def save_to_db(user_id, session_id, role, content):
    async with get_session()() as db:

        msg = ChatMessage(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        db.add(msg)
        await db.commit()

async def get_chat_history(user_id: str, session_id: str, limit: int = 20, offset: int = 0):
    async with get_session()() as db:
        result = await db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.user_id == user_id,
                ChatMessage.session_id == session_id
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        rows = result.scalars().all()

        return [
            {
                "role": r.role,
                "content": r.content,
                "timestamp": r.created_at
            }
            for r in reversed(rows)  # return in correct order
        ]
    


