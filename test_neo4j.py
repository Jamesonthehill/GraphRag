from app.graph.neo4j_client import get_graph

graph = get_graph()

result = graph.query("RETURN 'Neo4j connected successfully' AS message")

print(result)