from app.graph.neo4j_client import get_graph

graph = get_graph()

print("=== Nodes ===")
nodes = graph.query("""
MATCH (n)
RETURN labels(n) AS labels, n.id AS id, n.name AS name, properties(n) AS props
LIMIT 50
""")
for row in nodes:
    print(row)

print("\n=== Relationships ===")
rels = graph.query("""
MATCH (a)-[r]->(b)
RETURN 
  labels(a) AS source_labels,
  a.id AS source_id,
  a.name AS source_name,
  type(r) AS relationship,
  labels(b) AS target_labels,
  b.id AS target_id,
  b.name AS target_name
LIMIT 50
""")
for row in rels:
    print(row)