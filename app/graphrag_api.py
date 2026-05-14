from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.query_graph import answer_with_graph

router = APIRouter(prefix="/api/graphrag", tags=["GraphRAG"])


class GraphRAGRequest(BaseModel):
    question: str


class GraphRAGResponse(BaseModel):
    answer: str


@router.post("/query", response_model=GraphRAGResponse)
def query_graphrag(request: GraphRAGRequest):
    answer = answer_with_graph(request.question)
    return GraphRAGResponse(answer=answer)