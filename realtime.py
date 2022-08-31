from logs.log_manager import LogManager
from neo4j import GraphDatabase
from typing import Dict
from log_filter import LogFilter
from graph_handler import GraphHandler
from neo4j_handler import Neo4jHandler
from settings import ENV
from json import loads
import sys


class RealTimeDrawer:

    graphDB_Driver = None

    def __init__(self, config: Dict, logger) -> None:
        """ initialize neo4j graphDB driver with given config"""
        self.parser = LogFilter()
        self.logger = logger
        self.neo = Neo4jHandler(config)
        self.graph = GraphHandler(self.neo, self. parser, self.logger)

    def draw(self, message: Dict):
        """ send request to neo4j server """
        # message = eval(message)
        result = self.graph.extract_node_edge_from_json(message["log"])
        # node_1 = ""
        # node_2 = ""
        # edge = {}
        node_1, node_2, edge = result
        node_1, node_2 = self.preprocess_node_names([node_1, node_2])
        with self.neo.graphDB_Driver.session() as graphDB_Session:
            nodes = graphDB_Session.run("MATCH (n:node) RETURN n ")
            node_names = [n[0]._properties['name'] for n in nodes]
            print("here")

            if node_1 not in node_names:
                self.neo.create_new_node(node_1)
            if node_2 not in node_names:
                self.neo.create_new_node(node_2)

            self.neo.create_new_edge(node_1, node_2, edge)

    def preprocess_node_names(self, nodes):
        """ extract node names """
        new_nodes = []
        for i, node_name in enumerate(nodes):
            try:
                first_char = int(node_name[0])
                new_nodes.append(f"_{node_name}")
            except Exception as e:
                print(f"{e}")
                new_nodes.append(node_name)

        return new_nodes


def main(log):
    r = RealTimeDrawer(
        {
            "uri": "bolt://localhost:7687",
            "userName": "neo4j",
            "password": "test"
        },
        LogManager()

    )
    r.draw(log)


if __name__ == "__main__":
    print(sys.argv)
    log_data = """{
        "log": {
            "host": "4f33df1f5cc2",
            "host_ip": "172.17.0.2",
            "program_name": "proxy-server",
            "client_ip": "172.17.0.1",
            "remote_addr": "172.17.0.1",
            "date_time": "2022-04-03 14:01:17.678899",
            "method": "GET",
            "path": "/healthcheck",
            "protocol": "HTTP/1.0",
            "status_int": 200,
            "referer": "-",
            # "user_agent": "curl/7.68.0",
            "user_agent": "account-server",
            "auth_token": "-",
            "bytes_recvd": 0,
            "bytes_sent": 0,
            "client_etag": "-",
            "transaction_id": "txdxxxx",
            "headers": [
                "Host: 172.17.0.2:8080",
                "User-Agent: curl/7.68.0",
                "Accept: */*",
                "Content-Type: "
            ],
            "request_time": "0.0007",
            "source": "-",
            "log_info": "-",
            "start_time": "164.6",
            "end_time": "164.7",
            "policy_index": "-"
        }
    }"""
    main(log_data)
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(
                """
                draw corresponding graph realtime
                python3 realtime.py <tokenized log line in JSON format>
                """
            )
        else:
            log_data = sys.argv[1]
            main(log_data)
    else:
        print(
            """
            please provide log data
            """
        )
