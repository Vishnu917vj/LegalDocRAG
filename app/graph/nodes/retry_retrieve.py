from app.graph.state import GraphState


def retry_retrieve(state: GraphState):

    return {
        "retry_count": state["retry_count"] + 1
    }