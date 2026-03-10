from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


# ---- State ----
class State(TypedDict):
    prompt: str
    analysis: str
    clarified: str
    approved: bool


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ---- Nodes ----
def analyze(state: State) -> State:
    response = llm.invoke(
        [
            SystemMessage(content="Phân tích ý định và điểm chưa rõ trong prompt."),
            HumanMessage(content=state["prompt"]),
        ]
    )
    state["analysis"] = response.content
    return state


def clarify(state: State) -> State:
    response = llm.invoke(
        [
            SystemMessage(content="Viết lại prompt rõ ràng, đầy đủ hơn."),
            HumanMessage(content=state["prompt"]),
        ]
    )
    state["clarified"] = response.content
    return state


def human_review(state: State) -> State:
    print("\n--- Prompt đã làm rõ ---")
    print(state["clarified"])
    user_input = input("\nBạn có duyệt không? (y/n): ")

    state["approved"] = user_input.lower() == "y"
    return state


def main():
    # with log_request_to_openai():
    # ---- Graph ----
    graph = StateGraph(State)

    graph.add_node("analyze", analyze)
    graph.add_node("clarify", clarify)
    graph.add_node("review", human_review)

    graph.set_entry_point("analyze")
    graph.add_edge("analyze", "clarify")
    graph.add_edge("clarify", "review")

    # Nếu duyệt → kết thúc, nếu không → quay lại clarify
    graph.add_conditional_edges(
        "review",
        lambda s: "end" if s["approved"] else "clarify",
        {"end": END, "clarify": "clarify"},
    )

    app = graph.compile()

    # ---- Run ----
    initial_state = {
        "prompt": input("Nhập prompt: "),
        "analysis": "",
        "clarified": "",
        "approved": False,
    }

    app.invoke(initial_state)


if __name__ == "__main__":
    main()
