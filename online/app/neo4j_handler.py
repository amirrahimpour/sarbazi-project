"""
this file contains handlers for interacting with Neo4j
"""
from neo4j import GraphDatabase
from typing import Dict


class Neo4jHandler:
    """neo4j handler

    this class handles neo4j operations
    """

    graphDB_Driver = None

    def __init__(self, config: Dict) -> None:
        """ initialize neo4j graphDB driver with given config"""
        uri = config["uri"]
        userName = config["userName"]
        password = config["password"]
        self.graphDB_Driver = GraphDatabase.driver(
            uri, 
            auth=(
                userName,
                password
            )
        )

    def create_new_node(self, node: str) -> str:
        """create new node named (node)

        :param node: node name
        :return: node creation query
        """
        create_node = (
            "CREATE \n" 
            + f"({node}:node " 
            + "{ name: " 
            + f'"{node}"' 
            + "})"
        )
        with self.graphDB_Driver.session() as graphDB_Session:
            graphDB_Session.run(create_node)

        return create_node

    def create_new_edge(self, node_1: str, node_2: str, edge: Dict) -> str:
        """create new edge from node_1 to node_2

        :param node_1: source node
        :param node_2: destination node
        :param edge: edge properties
        :return: edge creation query
        """
        string = ""

        for i, key in enumerate(edge.keys()):
            if isinstance(edge[key], list):
                continue
            string += f"{key}: " + f"'{edge[key]}', "

        string = string[0:-2]  # to avoid the final ', ' in the string

        create_edge = (
            "MATCH (u:node {name:"
            + f"'{node_1}'"
            + "}), (r: node {name: "
            + f"'{node_2}'"
            + "}) "
            + f"CREATE(u)-[:{edge['label']}"
            + " { "
            + string
            + " }]->(r)"
        )

        with self.graphDB_Driver.session() as graphDB_Session:
            graphDB_Session.run(create_edge)

        return create_edge

    def clear_graph(self) -> None:
        """ clear the graph"""

        cqldelete1 = "match (a) -[r] -> () delete a, r"
        cqldelete2 = "match (a) delete a"
        with self.graphDB_Driver.session() as graphDB_Session:
            graphDB_Session.run(cqldelete1)
            graphDB_Session.run(cqldelete2)

    def delete_edge(self, new_gte) -> None:
        """ delete edges with datetime older than new_gte from the graph """
        
        cql_delete_edge = f"""
        MATCH p=()-[r]->()
        where datetime(r.datetime) <= datetime(\"{new_gte}\")
        delete r
        """
        with self.graphDB_Driver.session() as graphDB_Session:
            graphDB_Session.run(cql_delete_edge)
                
        

