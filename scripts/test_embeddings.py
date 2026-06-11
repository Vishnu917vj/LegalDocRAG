from app.services.embedding_service import EmbeddingService

embedder = EmbeddingService()

vector = embedder.embed_query(
    "When was the agreement signed?"
)

print(len(vector))
print(vector[:5])