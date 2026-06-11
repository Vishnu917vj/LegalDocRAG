from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService

embedder = EmbeddingService()
pinecone = PineconeService()

query = "When was the agreement signed?"

query_embedding = embedder.embed_query(query)

results = pinecone.search(
    query_embedding,
    top_k=3
)

for match in results["matches"]:
    print("-" * 50)
    print(match["score"])
    print(match["metadata"]["text"])