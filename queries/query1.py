from neo4j import GraphDatabase
import json

graphDB_Driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test"))
query = """
    MATCH (n)-[r:S_GET_P{label:"S_GET_P", referer:"-"}]->(m) RETURN  n,m,r,r.referer
"""

query3 = """MATCH (n)-[r:S_GET_P{label:"S_GET_P", status_int:"200"}]->(m) RETURN  n,m,r, r.status_int"""
query2 = """MATCH (n)-[r:S_PUT_P*]->(m) WHERE all(a in r where a.label="S_PUT_P") RETURN  n,m,r"""

with graphDB_Driver.session() as graphDB_Session:
    response = graphDB_Session.run(query)
    data = response.data()
    graph = response.graph()
    for n in response:
        print(n)
    for rel in graph.relationships:
        print(rel._properties)

print("here")
