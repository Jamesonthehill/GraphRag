from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.graph.neo4j_client import get_graph

load_dotenv()


def extract_search_term(question: str) -> str:
    question_lower = question.lower()

    known_terms = ["graphrag", "neo4j", "rag", "langchain"]

    for term in known_terms:
        if term in question_lower:
            return term

    return ""


def retrieve_graph_context(question: str):
    graph = get_graph()
    search_term = extract_search_term(question)

    if not search_term:
        return []

    records = graph.query(
        """
        MATCH (a)-[r]->(b)
        WHERE toLower(a.id) CONTAINS $search_term
        RETURN a.id AS source, type(r) AS relationship, b.id AS target
        """,
        {"search_term": search_term}
    )

    return records


def answer_with_graph(question: str) -> str:
    records = retrieve_graph_context(question)

    if not records:
        return "I could not find relevant graph context."

    context = "\n".join(
        f"{row['source']} -[{row['relationship']}]-> {row['target']}"
        for row in records
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
Use only the graph context below to answer the question.

Graph context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content