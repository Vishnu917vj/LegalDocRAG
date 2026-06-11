from app.graph.workflow import build_graph

graph = build_graph()

state = {
    "question": "When was the agreement signed?",
    "retrieved_chunks": [],
    "is_relevant": False,
    "answer": "",
    "citations": [],
    "retry_count": 0
}

result = graph.invoke(
    state
)

print(result)