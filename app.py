from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)


# ==========================
# STATE
# ==========================

class JobState(TypedDict):

    name: str
    role: str
    experience_years: int
    decision: str


# ==========================
# NODE 1
# ==========================

def receive_application(state):

    print("\nReceiving Application...")

    print(f"Name : {state['name']}")
    print(f"Role : {state['role']}")

    return {
        "name": state["name"],
        "role": state["role"]
    }


# ==========================
# NODE 2
# ==========================

def screen_resume(state):

    print("\nScreening Resume...")

    if state["experience_years"] > 2:

        return {
            "decision": "Selected"
        }

    return {
        "decision": "Rejected"
    }


# ==========================
# NODE 3
# ==========================

def send_decision(state):

    print("\nSending Decision...")

    print(
        f"Candidate "
        f"{state['name']} "
        f"is "
        f"{state['decision']}"
    )

    return state


# ==========================
# GRAPH
# ==========================

builder = StateGraph(JobState)

builder.add_node(
    "receive_application",
    receive_application
)

builder.add_node(
    "screen_resume",
    screen_resume
)

builder.add_node(
    "send_decision",
    send_decision
)

builder.set_entry_point(
    "receive_application"
)

builder.add_edge(
    "receive_application",
    "screen_resume"
)

builder.add_edge(
    "screen_resume",
    "send_decision"
)

builder.add_edge(
    "send_decision",
    END
)

graph = builder.compile()


# ==========================
# INPUT
# ==========================

result = graph.invoke(
    {
        "name": "Charan",
        "role": "Data Analyst",
        "experience_years": 3
    }
)

print("\nFinal State:")
print(result)