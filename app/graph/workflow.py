from langgraph.graph import StateGraph
from langgraph.graph import END

from app.graph.state import GraphState

from app.graph.nodes.retrieve import retrieve
from app.graph.nodes.relevance_check import relevance_check
from app.graph.nodes.generate_answer import generate_answer
from app.graph.nodes.no_answer import no_answer
from app.graph.nodes.retry_retrieve import retry_retrieve
from app.graph.routers.retry_router import retry_router

from app.graph.routers.relevance_router import (
    relevance_router
)


def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node(
        "retrieve",
        retrieve
    )

    workflow.add_node(
        "relevance_check",
        relevance_check
    )

    workflow.add_node(
        "generate_answer",
        generate_answer
    )

    workflow.add_node(
        "no_answer",
        no_answer
    )

    workflow.add_node(
    "retry_retrieve",
    retry_retrieve
)

    workflow.set_entry_point(
        "retrieve"
    )

    workflow.add_edge(
        "retrieve",
        "relevance_check"
    )

    workflow.add_conditional_edges(
    "relevance_check",
    relevance_router,
    {
        "generate_answer": "generate_answer",
        "retry_retrieve": "retry_retrieve"
    }
)
    workflow.add_conditional_edges(
    "retry_retrieve",
    retry_router,
    {
        "retrieve": "retrieve",
        "no_answer": "no_answer"
    }
)

    workflow.add_edge(
        "generate_answer",
        END
    )

    workflow.add_edge(
        "no_answer",
        END
    )

    return workflow.compile()