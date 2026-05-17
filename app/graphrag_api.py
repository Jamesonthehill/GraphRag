from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.query_graph import answer_with_graph
from app.db import save_chat

router = APIRouter(prefix="/api/graphrag", tags=["GraphRAG"])


class GraphRAGRequest(BaseModel):
    question: str


class GraphRAGResponse(BaseModel):
    answer: str


@router.post("/query", response_model=GraphRAGResponse)
def query_graphrag(request: GraphRAGRequest):
    answer = answer_with_graph(request.question)

    save_chat(
        user_input=request.question,
        model_output=answer
    )

    return GraphRAGResponse(answer=answer)