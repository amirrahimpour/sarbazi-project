"""
    this file contains methods for creating graph edges and nodes
"""
server_names = {
    "172.24.1.194": "cloud1",
    "172.24.1.195": "cloud2",
    "172.24.1.196": "cloud3",
}


class GraphHandler:
    """
    graph handler class for creating graph
    """

    def __init__(self, neo, parser, logger) -> None:
        self.neo = neo  # Neo4j Driver
        self.nodes = []  # graph node names to avoid repeatition
        self.edges = {}  # graph edge names (obsolete)
        self.parser = parser  # log parser object
        self.logger = logger  # logger object (for unprocessible lines)

    def create_graph(self, lines):
        """
        create a graph based on input log lings
        """
        self.neo.clear_graph()
        for i, _line in enumerate(lines):
            result = self.extract_node_edge_from_log(_line)
            if None in result:
                self.logger.error(_line)    # log the unprocessible line
                continue

            node_1, node_2, edge = result
            if "none" in edge["label"]:
                self.logger.error(_line)    # log the unprocessible line
                continue

            if node_1 not in self.nodes:
                self.neo.create_new_node(node_1)
                self.nodes.append(node_1)
            if node_2 not in self.nodes:
                self.neo.create_new_node(node_2)
                self.nodes.append(node_2)

            self.neo.create_new_edge(node_1, node_2, edge)
            # if f"{node_1}-{node_2}" in self.edges:
            # if edge["label"] not in self.edges[f"{node_1}-{node_2}"]:
            # self.neo.create_new_edge(node_1, node_2, edge)
            # self.edges[f"{node_1}-{node_2}"].append(edge["label"])
            # else:
            # pass
            # else:
            # self.neo.create_new_edge(node_1, node_2, edge)
            # self.edges[f"{node_1}-{node_2}"] = []
            # self.edges[f"{node_1}-{node_2}"].append(edge["label"])

    def extract_node_edge_from_log(self, line):
        """
        extract nodes and edges from log lines
        """
        try:
            parsed_log = self.parser.parse_log(line)
            node_1 = parsed_log["remote_addr"]
            node_2 = parsed_log["destination_server"]
            source, method, destination = self.get_source_destination(parsed_log)
            edge_label = f"{source}_{method}_{destination}"

        except Exception as e:
            self.logger.error(line)
            # print(f"error: {e}, log line: {line}")
            return None, None, None

        try:
            if node_1 == "-" or node_2 == "-":
                return None, None, None

            node_1 = node_1.replace("m-", "")
            node_2 = node_2.replace("m-", "")
            if node_1 in server_names.keys():
                node_1 = server_names[node_1]
            if node_2 in server_names.keys():
                node_2 = server_names[node_2]
            if "." in node_1:
                node_1 = f"IP_{node_1}".replace(".", "_")
            if "." in node_2:
                node_2 = f"IP_{node_2}".replace(".", "_")

        except Exception as e:
            pass
            # print(f"error: {e}, log line: {line}")
            # print(f"parsed log: {parsed_log}")

        if "STDERR" in line:
            _type = "ERR"
        else:
            _type = "INFO"

        message = parsed_log["message"][0:90].replace("'", "")
        edge = {"type": _type, "label": edge_label, "message": message}
        parsed_log["type"] = _type
        parsed_log["label"] = edge_label
        parsed_log["message"] = message
        
        return node_1, node_2, parsed_log

    def get_source_destination(self, parsed_log):
        """
        map service names to predefined abbreviations
        """
        mapping = {
            "proxy": "P",
            "account": "A",
            "container": "C",
            "object": "O",
            "Swift": "S",
            "python-swiftclient-3.5.0": "S",
            "none": "none",
        }
        source = mapping[parsed_log["source_service"]]
        destination = mapping[parsed_log["program_name"]]

        method = parsed_log["method"]
        return source, method, destination
