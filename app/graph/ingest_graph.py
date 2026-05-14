from pathlib import Path
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

from app.graph.neo4j_client import get_graph

load_dotenv()


def load_local_documents():
    text_path = Path("app/data/sample.txt")
    text = text_path.read_text(encoding="utf-8")

    return [
        Document(
            page_content=text,
            metadata={"source": str(text_path)}
        )
    ]


def chunk_documents():
    raw_documents = load_local_documents()

    text_splitter = TokenTextSplitter(
        chunk_size=512,
        chunk_overlap=64,
    )

    documents = text_splitter.split_documents(raw_documents)

    print(f"Split into {len(documents)} chunks.")
    return documents


def build_graph():
    graph = get_graph()
    documents = chunk_documents()

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    llm_transformer = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=["Concept", "Technology", "Database", "Method"],
        allowed_relationships=[
            "USES",
            "STORES",
            "RETRIEVES",
            "CONNECTS",
            "RELATED_TO",
            "PART_OF",
        ],
    )

    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    for doc in graph_documents:
        print("Nodes:", doc.nodes)
        print("Relationships:", doc.relationships)
        print("---")

    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True,
    )

    print("Graph documents added to Neo4j.")


if __name__ == "__main__":
    build_graph()