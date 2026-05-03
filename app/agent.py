from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph, END
import logging

from app.services.llm import generate_response

logger = logging.getLogger("app")


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class ChatState(TypedDict):
    messages: List[Message]


async def llm_node(state: ChatState):
    messages = state["messages"][-10:]  # limit history

    try:
        logger.info(f"LLM call with {len(messages)} messages")
        response = await generate_response(messages)
    except Exception as e:
        logger.error(f"LLM error: {str(e)}")
        response = "Sorry, something went wrong."

    return {
        "messages": messages + [{"role": "assistant", "content": response}]
    }


builder = StateGraph(ChatState)

builder.add_node("llm", llm_node)
builder.set_entry_point("llm")
builder.add_edge("llm", END)

graph = builder.compile()