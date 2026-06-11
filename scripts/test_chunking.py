from app.services.chunking_service import ChunkingService

chunker = ChunkingService()

text = """
The agreement was signed on March 12 2024.

The agreement expires on July 15 2025.

Any disputes shall be handled by Delta Court.
""" * 20

chunks = chunker.chunk_document(
    text=text,
    source="test.txt"
)

print(f"Total Chunks: {len(chunks)}")

for chunk in chunks:
    print(chunk)