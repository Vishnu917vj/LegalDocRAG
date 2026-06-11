from app.graph.nodes.generate_answer import generate_answer

state = {
    "question": "When was the agreement signed?",
    "retrieved_chunks": [
        {
            "chunk_id": "agreement.txt::chunk_0",
            "source": "agreement.txt",
            "text": "The agreement was signed on March 12 2024.",
            "score": 0.91
        }
    ],
    "is_relevant": True,
    "answer": "",
    "citations": [],
    "retry_count": 0
}

result = generate_answer(state)

print(result)