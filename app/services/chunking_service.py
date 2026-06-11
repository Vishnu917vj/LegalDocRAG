from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:
    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=100
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk_document(
        self,
        text: str,
        source: str
    ):
        chunks = self.splitter.split_text(text)

        return [
            {
                "chunk_id": f"{source}_chunk_{i}",
                "source": source,
                "text": chunk
            }
            for i, chunk in enumerate(chunks)
        ]