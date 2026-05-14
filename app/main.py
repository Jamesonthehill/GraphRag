from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.graphrag_api import router as graphrag_router

app = FastAPI(title="GraphRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphrag_router)


@app.get("/")
def root():
    return {"message": "GraphRAG API is running"}