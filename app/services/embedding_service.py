from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def embed_documents(
        self,
        documents: List[str]
    ) -> List[List[float]]:
        """
        Embed document chunks for storage.
        """

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    def embed_query(
        self,
        query: str
    ) -> List[float]:
        """
        Embed user query for retrieval.
        """

        formatted_query = (
            "Represent this sentence for searching relevant passages: "
            + query
        )

        embedding = self.model.encode(
            formatted_query,
            normalize_embeddings=True
        )

        return embedding.tolist()