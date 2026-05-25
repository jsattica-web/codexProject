from typing import TypedDict, Annotated, Sequence
import operator
import os

from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class AgentState(TypedDict):
    order: dict
    messages: Annotated[Sequence[BaseMessage], operator.add]


@tool
def cancel_order(order_id: str) -> str:
    """Cancel an order that has not been shipped yet."""
    return f"Order {order_id} has been canceled."


def _build_llm():
    """
    Default is free local inference via Ollama.

    Env options:
    - LLM_PROVIDER=ollama|openai (default: ollama)
    - LLM_MODEL=<model name>
    - OPENAI_API_KEY is only required when LLM_PROVIDER=openai
    """
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        return init_chat_model(model=model, model_provider="openai", temperature=0)

    # Free local default (no OpenAI billing)
    model = os.getenv("LLM_MODEL", "llama3.1:8b")
    return init_chat_model(model=model, model_provider="ollama", temperature=0)


def call_model(state):
    msgs = state["messages"]
    order = state.get("order", {"order_id": "UNKNOWN"})

    llm = _build_llm()
    llm_with_tools = llm.bind_tools([cancel_order])

    prompt = (
        "You are an e-commerce support agent. "
        f"Order ID: {order['order_id']}. "
        "If the customer asks to cancel, call cancel_order(order_id). "
        "Then send a short confirmation message."
    )

    full = [SystemMessage(content=prompt)] + list(msgs)

    first = llm_with_tools.invoke(full)
    out = [first]

    if getattr(first, "tool_calls", None):
        tc = first.tool_calls[0]
        result = cancel_order.invoke(tc["args"])
        out.append(ToolMessage(content=result, tool_call_id=tc["id"]))

        second = llm.invoke(full + out)
        out.append(second)

    return {"messages": out}


def construct_graph():
    g = StateGraph(AgentState)
    g.add_node("assistant", call_model)
    g.set_entry_point("assistant")
    return g.compile()


graph = construct_graph()


if __name__ == "__main__":
    example_order = {"order_id": "B73973"}
    convo = [HumanMessage(content="Please cancel order #B73973.")]
    result = graph.invoke({"order": example_order, "messages": convo})

    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")
