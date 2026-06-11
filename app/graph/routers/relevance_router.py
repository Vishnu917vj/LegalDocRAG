def relevance_router(state):

    if state["is_relevant"]:
        return "generate_answer"

    return "retry_retrieve"