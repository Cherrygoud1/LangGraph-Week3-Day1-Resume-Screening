from typing import TypedDict
from langgraph.graph import StateGraph, END


class ResumeState(TypedDict):
    candidate_name: str
    experience_years: int
    attempts: int
    decision: str


def screen_resume(state):

    print(
        f"\nScreening Resume..."
    )

    print(
        f"Experience: {state['experience_years']} Years"
    )

    return state


def improve_resume(state):

    print(
        "\nImproving Resume..."
    )

    state["experience_years"] += 1
    state["attempts"] += 1

    return state


def shortlisted(state):

    print(
        "\nCandidate Shortlisted"
    )

    state["decision"] = "Selected"

    return state


def rejected(state):

    print(
        "\nCandidate Rejected"
    )

    state["decision"] = "Rejected"

    return state


def route_resume(state):

    if state["experience_years"] >= 3:
        return "selected"

    if state["attempts"] >= 3:
        return "rejected"

    return "improve"


builder = StateGraph(
    ResumeState
)

builder.add_node(
    "screen",
    screen_resume
)

builder.add_node(
    "improve",
    improve_resume
)

builder.add_node(
    "selected",
    shortlisted
)

builder.add_node(
    "rejected",
    rejected
)

builder.set_entry_point(
    "screen"
)

builder.add_conditional_edges(
    "screen",
    route_resume
)

builder.add_edge(
    "improve",
    "screen"
)

builder.add_edge(
    "selected",
    END
)

builder.add_edge(
    "rejected",
    END
)

graph = builder.compile()

result = graph.invoke(
    {
        "candidate_name": "Charan",
        "experience_years": 1,
        "attempts": 0,
        "decision": ""
    }
)

print("\nFinal Output:")
print(result)