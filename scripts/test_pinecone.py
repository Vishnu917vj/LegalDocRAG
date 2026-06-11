from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService

embedder = EmbeddingService()
pinecone = PineconeService()

text = "The agreement was signed on March 12 2024"

embedding = embedder.embed_documents(
    [text]
)[0]

vectors = [
    {
        "id": "chunk_1",
        "values": embedding,
        "metadata": {
            "source": "test.txt",
            "chunk_id": "chunk_1",
            "text": text
        }
    }
]

pinecone.upsert_vectors(vectors)

print("Vector inserted.")