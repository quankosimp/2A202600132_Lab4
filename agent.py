import os
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from tools import calculate_budget, search_flights, search_hotels

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()


def create_llm() -> ChatOpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "Thiếu API key. Hãy đặt OPENROUTER_API_KEY hoặc OPENAI_API_KEY trong file .env."
        )

    model = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
    site_url = os.getenv("OPENROUTER_SITE_URL", "http://localhost")
    app_name = os.getenv("OPENROUTER_APP_NAME", "TravelBuddy")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": site_url,
            "X-Title": app_name,
        },
    )


SYSTEM_PROMPT = load_system_prompt()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def get_tools_list():
    return [search_flights, search_hotels, calculate_budget]


@lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    return create_llm()


@lru_cache(maxsize=1)
def get_llm_with_tools():
    return get_llm().bind_tools(get_tools_list())


def agent_node(state: AgentState):
    messages = list(state["messages"])
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = get_llm_with_tools().invoke(messages)

    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']} ({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")

    return {"messages": [response]}


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)

    tool_node = ToolNode(get_tools_list())
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder.compile()


@lru_cache(maxsize=1)
def get_graph():
    return build_graph()


def run_agent(user_input: str):
    return get_graph().invoke({"messages": [("human", user_input)]})


if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        result = run_agent(user_input)
        final = result["messages"][-1]

        print(f"\nTravelBuddy: {final.content}")
