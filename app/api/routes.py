from fastapi import APIRouter

from app.models.request_models import AskRequest
from app.models.response_models import AskResponse

from app.graph.graph_instance import graph


router = APIRouter()


@router.post(
    "/ask",
    response_model=AskResponse
)
def ask_question(
    request: AskRequest
):

    initial_state = {
        "question": request.question,
        "retrieved_chunks": [],
        "is_relevant": False,
        "answer": "",
        "citations": [],
        "retry_count": 0
    }

    result = graph.invoke(
        initial_state
    )

    return AskResponse(
        answer=result["answer"],
        citations=result["citations"]
    )