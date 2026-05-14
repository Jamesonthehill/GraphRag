import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

def get_graph() -> Neo4jGraph:
    return Neo4jGraph(
        url=os.environ["NEO4J_URI"],
        username=os.environ["NEO4J_USERNAME"],
        password=os.environ["NEO4J_PASSWORD"],
    )