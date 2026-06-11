from app.graph.state import GraphState
from app.services.llm_service import LLMService


llm = LLMService()


def relevance_check(state: GraphState):

    retrieved_chunks = state["retrieved_chunks"]

    if not retrieved_chunks:
        return {
            "is_relevant": False
        }

    question = state["question"]

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    prompt = f"""
You are a retrieval evaluator.

Question:
{question}

Retrieved Context:
{context}

Can the context answer the question?

Reply with ONLY:

YES

or

NO
"""

    response = llm.invoke(prompt)

    is_relevant = (
        "YES" in response.upper()
    )

    return {
        "is_relevant": is_relevant
    }