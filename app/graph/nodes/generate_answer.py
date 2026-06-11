from app.graph.state import GraphState
from app.services.llm_service import LLMService


llm = LLMService()


def generate_answer(state: GraphState):

    question = state["question"]
    chunks = state["retrieved_chunks"]

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""
You are a legal document QA assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
say:

"I could not find the answer in the provided documents."

Question:
{question}

Context:
{context}
"""

    answer = llm.invoke(prompt)

    citations = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"]
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "citations": citations
    }