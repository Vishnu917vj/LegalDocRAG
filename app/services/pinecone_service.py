from pinecone import Pinecone
from app.config.settings import settings


class PineconeService:
    def __init__(self):
        self.pc = Pinecone(
            api_key=settings.PINECONE_API_KEY
        )

        self.index = self.pc.Index(
            settings.PINECONE_INDEX_NAME
        )

    def upsert_vectors(
        self,
        vectors: list
    ):
        """
        Insert vectors into Pinecone.
        """

        self.index.upsert(
            vectors=vectors
        )

    def search(
        self,
        query_vector: list,
        top_k: int = 5
    ):
        """
        Search Pinecone.
        """

        return self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )