MAX_RETRIES = 2


def retry_router(state):

    print("Current retry count:", state["retry_count"])

    if state["retry_count"] >= MAX_RETRIES:
        print("Going to no_answer")
        return "no_answer"

    print("Retrying retrieval")
    return "retrieve"