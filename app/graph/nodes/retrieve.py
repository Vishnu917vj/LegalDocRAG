from app.graph.state import GraphState
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService


embedder = EmbeddingService()
pinecone = PineconeService()


TOP_K = 5
MIN_SCORE = 0.50


def retrieve(state: GraphState):
    question = state["question"]

    query_embedding = embedder.embed_query(
        question
    )


    results = pinecone.search(
        query_vector=query_embedding,
        top_k=TOP_K
    )

    retrieved_chunks = []

    for match in results["matches"]:
        if match["score"] < MIN_SCORE:
            continue

        retrieved_chunks.append(
            {
                "chunk_id": match["metadata"]["chunk_id"],
                "source": match["metadata"]["source"],
                "text": match["metadata"]["text"],
                "score": match["score"],
            }
        )

    return {
        "retrieved_chunks": retrieved_chunks
    }