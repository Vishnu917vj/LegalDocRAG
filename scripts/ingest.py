from pathlib import Path

from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService


DATA_DIR = Path("data/raw")


def load_documents():
    documents = []

    for pattern in ["*.txt", "*.md"]:

        for file_path in DATA_DIR.glob(pattern):

            text = file_path.read_text(
                encoding="utf-8"
            )

            documents.append(
                {
                    "source": file_path.name,
                    "text": text
                }
            )

    return documents


def main():
    print("Loading services...")

    chunker = ChunkingService(
        chunk_size=800,
        chunk_overlap=150
    )

    embedder = EmbeddingService()

    pinecone = PineconeService()

    print("Loading documents...")

    documents = load_documents()

    print(f"Found {len(documents)} documents")

    total_chunks = 0

    for document in documents:

        source = document["source"]
        text = document["text"]

        chunks = chunker.chunk_document(
            text=text,
            source=source
        )

        print(
            f"{source}: {len(chunks)} chunks"
        )

        chunk_texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = embedder.embed_documents(
            chunk_texts
        )

        vectors = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):
            vectors.append(
                {
                    "id": chunk["chunk_id"],
                    "values": embedding,
                    "metadata": {
                        "source": chunk["source"],
                        "chunk_id": chunk["chunk_id"],
                        "text": chunk["text"]
                    }
                }
            )

        pinecone.upsert_vectors(
            vectors
        )

        total_chunks += len(chunks)

    print()
    print("=" * 50)
    print(
        f"Ingestion complete."
    )
    print(
        f"Documents: {len(documents)}"
    )
    print(
        f"Chunks: {total_chunks}"
    )
    print("=" * 50)


if __name__ == "__main__":
    main()