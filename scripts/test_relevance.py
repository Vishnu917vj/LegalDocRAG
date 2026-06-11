from app.graph.nodes.relevance_check import relevance_check

state = {
    "question": "When was the agreement signed?",
    "retrieved_chunks": [
        {
            "chunk_id": "1",
            "source": "test.txt",
            "text": "The agreement was signed on March 12 2024.",
            "score": 0.91
        }
    ],
    "is_relevant": False,
    "answer": "",
    "citations": [],
    "retry_count": 0
}

print(
    relevance_check(state)
)