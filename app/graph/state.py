from typing import TypedDict, List, Dict, Any


class GraphState(TypedDict):
    question: str

    retrieved_chunks: List[Dict[str, Any]]

    is_relevant: bool

    answer: str

    citations: List[Dict[str, str]]

    retry_count: int