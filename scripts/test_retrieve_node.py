from app.graph.nodes.retrieve import retrieve

state = {
    "question": "When was the agreement signed?",
    "retrieved_chunks": [],
    "is_relevant": False,
    "answer": "",
    "citations": [],
    "retry_count": 0
}

result = retrieve(state)

print(result)