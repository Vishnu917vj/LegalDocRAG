from app.graph.state import GraphState


def no_answer(state: GraphState):

    return {
        "answer": (
            "I could not find the answer "
            "in the provided documents."
        ),
        "citations": []
    }