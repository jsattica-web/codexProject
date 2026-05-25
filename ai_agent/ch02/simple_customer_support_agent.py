from typing import TypedDict, Annotated, Sequence
import operator
import os
import re

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
    """배송되지 않은 주문을 취소합니다."""
    # (여기서 실제 백엔드 API를 호출합니다)
    return f"주문 {order_id}이(가) 취소되었습니다."


def _build_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        return init_chat_model(model=model, model_provider="openai", temperature=0)

    model = os.getenv("LLM_MODEL", "llama3.2:1b")
    return init_chat_model(model=model, model_provider="ollama", temperature=0)


def _needs_cancel(messages: Sequence[BaseMessage]) -> bool:
    text = "\n".join(str(getattr(m, "content", "")) for m in messages).lower()
    keywords = ["cancel", "cancellation", "취소", "주문 취소"]
    return any(k in text for k in keywords)


def _extract_order_id(messages: Sequence[BaseMessage], default_id: str) -> str:
    text = "\n".join(str(getattr(m, "content", "")) for m in messages)
    m = re.search(r"#?([A-Za-z]\d{4,}|\d{4,})", text)
    return m.group(1) if m else default_id


def _extract_order_id_from_tool_args(tool_args, default_id: str) -> str:
    """Normalize inconsistent tool args emitted by small local models."""
    if isinstance(tool_args, dict):
        if "order_id" in tool_args and tool_args["order_id"]:
            return str(tool_args["order_id"])

        # Sometimes args can be {"<random text>": {"order_id": "B73973"}}
        for v in tool_args.values():
            if isinstance(v, dict) and "order_id" in v and v["order_id"]:
                return str(v["order_id"])

        # Last resort: parse from serialized dict
        m = re.search(r"#?([A-Za-z]\d{4,}|\d{4,})", str(tool_args))
        if m:
            return m.group(1)

    if isinstance(tool_args, str):
        m = re.search(r"#?([A-Za-z]\d{4,}|\d{4,})", tool_args)
        if m:
            return m.group(1)

    return default_id


def call_model(state):
    msgs = state["messages"]
    order = state.get("order", {"order_id": "UNKNOWN"})

    llm = _build_llm()
    llm_with_tools = llm.bind_tools([cancel_order])

    prompt = (
        f'''당신은 이커머스 지원 에이전트입니다.
        주문 ID: {order['order_id']}
        고객이 취소를 요청하면 cancel_order(order_id)를 호출하고
        간단한 확인 메시지를 보내세요.
        그렇지 않으면 일반적으로 응답하세요.'''
    )

    full = [SystemMessage(content=prompt)] + list(msgs)

    first = llm_with_tools.invoke(full)
    out = [first]

    # Normal tool-call path
    if getattr(first, "tool_calls", None):
        tc = first.tool_calls[0]
        oid = _extract_order_id_from_tool_args(tc.get("args"), order.get("order_id", "UNKNOWN"))
        result = cancel_order.invoke({"order_id": oid})
        out.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        second = llm.invoke(full + out)
        out.append(second)
        return {"messages": out}

    # Fallback for small local models that skip explicit tool_calls
    if _needs_cancel(msgs):
        oid = _extract_order_id(msgs, order.get("order_id", "UNKNOWN"))
        result = cancel_order.invoke({"order_id": oid})
        out.append(ToolMessage(content=result, tool_call_id="manual-cancel-order"))
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
    convo = [HumanMessage(content="주문 #B73973를 취소해주세요.")]
    result = graph.invoke({"order": example_order, "messages": convo})

    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")

