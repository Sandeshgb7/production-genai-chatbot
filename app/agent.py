from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from app.services.llm import generate_response


# state definition
class ChatState(TypedDict):
    messages: List[dict]


# node: LLM
async def llm_node(state: ChatState):
    messages = state["messages"]

    response = await generate_response(messages)

    messages.append({"role": "assistant", "content": response})

    return {"messages": messages}


# build graph
builder = StateGraph(ChatState)

builder.add_node("llm", llm_node)

builder.set_entry_point("llm")

builder.add_edge("llm", END)

graph = builder.compile()