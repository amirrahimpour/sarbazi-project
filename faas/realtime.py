from logging import getLogger
from neo4j import GraphDatabase
from typing import Dict
from settings import ENV

class RealTimeDrawer:

    graphDB_Driver = None

    def __init__(self, config: Dict, logger) -> None:
        """ initialize neo4j graphDB driver with given config"""
        self.logger = logger
        self.graphDB_Driver = GraphDatabase.driver(
            config["uri"],
            auth=(
                config["userName"],
                config["password"]
            )
        )

    def extract_source_from_user_agent(self, user_agent):
        """ extract source service name from user-agent field """
        source = None
        if "server" in user_agent:
            source = ENV.mapping[user_agent.split("-server")[0]]
        elif "updater" in user_agent:
            source = ENV.mapping[user_agent.split("-updater")[0]]
            source += "U"
        else:
            source = "S"

        return source

    def extract_destination_from_line(self, line):
        """ extract program name from log """
        destination = None
        if "program_name" in line:
            program_name = line["program_name"]
        elif "programname" in line:
            program_name = line["programname"]
        else:
            return None

        if "server" in program_name:
            destination = ENV.mapping[
                program_name.split("-server")[0]
            ]
        elif "updater" in program_name:
            destination = ENV.mapping[
                program_name.split("-updater")[0]
            ]
            destination += "U"
        else:
            destination = "S"
        return destination

    def extract_method_from_line(self, line):
        """ extract method name from log """
        if "method" in line:
            method = line["method"]
        else:
            for _method in ENV.method_names:
                if _method in line["message"]:
                    return _method
        return method

    def extract_node_edge_from_json(self, line):
        """ extract node and edge information from log """
        if line["remote_addr"] in ENV.server_names:
            node_1 = ENV.server_names[line["remote_addr"]]
        else:
            node_1 = line["remote_addr"]
            if node_1 == "-":
                return None, None, None

        # node_2 = line["sysloghost"]
        if line["host"] in ENV.server_names:
            node_2 = ENV.server_names[line["host"]]
        else:
            node_2 = line["host"]

        source = self.extract_source_from_user_agent(line["user_agent"])
        destination = self.extract_destination_from_line(line)
        method = self.extract_method_from_line(line)
        edge = {
            "type": "INFO",
            "label": f"{source}_{method}_{destination}",
        }
        if "-" in node_1:
            node_1 = f"{node_1}".replace("-", "_")
        if "-" in node_2:
            node_2 = f"{node_2}".replace("-", "_")
        if "." in node_1:
            node_1 = f"IP_{node_1}".replace(".", "_")
        if "." in node_2:
            node_2 = f"IP_{node_2}".replace(".", "_")

        for key in line:
            if "@" not in key and key != "tags":
                edge[key] = line[key]

        return node_1, node_2, edge


    def draw(self, message: Dict):
        """ handle overall process """        
        node_1, node_2, edge = self.extract_node_edge_from_json(
            message
        )
        node_1 = f"_{node_1}"
        node_2 = f"_{node_2}"

        with self.graphDB_Driver.session() as graphDB_Session:
            string = ""

            for i, key in enumerate(edge.keys()):
                if isinstance(edge[key], list):
                    continue
                string += f"{key}: " + f"'{edge[key]}', "

            graphDB_Session.run(
                "MERGE \n" +
                f"({node_1}:node " + "{ name: " + f'"{node_1}"' + "})" +
                "MERGE \n" +
                f"({node_2}:node " + "{ name: " + f'"{node_2}"' + "})" +
                f"MERGE ({node_1})-[:{edge['label']}"
                + " { "
                + string[0:-2]
                + " }]->"
                + f"({node_2})"
            )
            print("done")

def main(log):
    """ script entrypoint """
    logger = getLogger("error_logger")
    r = RealTimeDrawer(
        {
            "uri": "bolt://localhost:7687",
            "userName": "neo4j",
            "password": "test"
        },
        logger
    )
    r.draw(log)