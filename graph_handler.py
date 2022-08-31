"""
    this file contains methods for creating graph edges and nodes
"""
from settings import ENV


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

    def create_graph_txt(self, lines):
        """
        create a graph based on input log lings
        """
        self.neo.clear_graph()              # clear the database
        for i, _line in enumerate(lines):   # iterate through each line
            result = self.extract_node_edge_from_log(_line)             # extract node and edge info from log line
            if None in result:
                self.logger.error(_line)    # log the unprocessible line
                continue

            node_1, node_2, edge = result
            if "none" in edge["label"]:
                self.logger.error(_line)    # log the unprocessible line
                continue

            if node_1 not in self.nodes:                                # check if node is not already present                            
                self.neo.create_new_node(node_1)
                self.nodes.append(node_1)
            if node_2 not in self.nodes:
                self.neo.create_new_node(node_2)
                self.nodes.append(node_2)

            self.neo.create_new_edge(node_1, node_2, edge)

    def create_graph_json(self, lines):
        """ create graph from json (list of dict objs)"""
        self.neo.clear_graph()                  # clear the database
        for i, _line in enumerate(lines):       # iterate through the log lines
            result = self.extract_node_edge_from_json(_line)            # extract node, edge info from log line
            if None in result:
                self.logger.error(_line)    # log the unprocessible line
                continue

            node_1, node_2, edge = result
            if "none" in edge["label"]:
                self.logger.error(_line)    # log the unprocessible line
                continue

            if node_1 not in self.nodes:                                # check if nodes are not already present
                self.neo.create_new_node(node_1)
                self.nodes.append(node_1)
            if node_2 not in self.nodes:
                self.neo.create_new_node(node_2)
                self.nodes.append(node_2)

            self.neo.create_new_edge(node_1, node_2, edge)              # send node, edge info to neo4j handler

    def extract_node_edge_from_log(self, line):
        """
        extract nodes and edges from log lines
        """
        try:
            parsed_log = self.parser.parse_log(line)                    # parse the log
            node_1 = parsed_log["remote_addr"]
            node_2 = parsed_log["destination_server"]
            source, method, destination = self.get_source_destination(      # get source, edge & destination info
                parsed_log)
            edge_label = f"{source}_{method}_{destination}"

        except Exception as e:
            self.logger.error(line)                                     # log the unprocessible
            # print(f"error: {e}, log line: {line}")
            return None, None, None

        try:
            if node_1 == "-" or node_2 == "-":                          # skip if node = -
                return None, None, None

            node_1 = node_1.replace("m-", "m_")
            node_2 = node_2.replace("m-", "m_")
            if node_1 in ENV.server_names.keys():                       # map IP to server names
                node_1 = ENV.server_names[node_1]
            if node_2 in ENV.server_names.keys():
                node_2 = ENV.server_names[node_2]
            if "." in node_1:                                           # replace special characters
                node_1 = f"IP_{node_1}".replace(".", "_")
            if "." in node_2:
                node_2 = f"IP_{node_2}".replace(".", "_")
            if "-" in node_1:
                node_1 = f"{node_1}".replace("-", "_")
            if "-" in node_2:
                node_2 = f"{node_2}".replace("-", "_")

        except Exception as e:
            pass
            # print(f"error: {e}, log line: {line}")
            # print(f"parsed log: {parsed_log}")

        if "STDERR" in line:                                           # separate ERROR & INFO lines
            _type = "ERR"
        else:
            _type = "INFO"

        message = parsed_log["message"][0:90].replace("'", "")         # truncate long messages

        parsed_log["type"] = _type
        parsed_log["label"] = edge_label
        parsed_log["message"] = message

        return node_1, node_2, parsed_log

    def get_source_destination(self, parsed_log):
        """
        map service names to predefined abbreviations
        """
        source = ENV.mapping[parsed_log["source_service"]]          # map IP to server names
        destination = ENV.mapping[parsed_log["program_name"]]

        method = parsed_log["method"]
        return source, method, destination

    def extract_source_from_user_agent(self, user_agent):
        source = None
        try:
            if "server" in user_agent:
                source = ENV.mapping[user_agent.split("-server")[0]]        # mapping for main services
            elif "updater" in user_agent:
                source = ENV.mapping[user_agent.split("-updater")[0]]       # mapping for side services
                source += "U"
            else:
                source = "S"                                                # other services notes as 'S'
        except Exception as e:
            print(f"error in extracting source from user agent: {e}")
            raise

        return source

    def extract_destination_from_line(self, line):
        destination = None
        if "program_name" in line:
            program_name = line["program_name"]
        elif "programname" in line:
            program_name = line["programname"]
        else:
            return None

        if "server" in program_name:
            destination = ENV.mapping[
                program_name.split("-server")[0]                        # map main service names
            ]
        elif "updater" in program_name:
            destination = ENV.mapping[
                program_name.split("-updater")[0]                       # map side service names
            ]
            destination += "U"
        else:
            destination = "S"                                           # other services notes as 'S'
        return destination

    def extract_method_from_line(self, line):
        """ extract method name """
        if "method" in line:
            method = line["method"]
        else:
            for _method in ENV.method_names:
                if _method in line["message"]:
                    return _method
        return method

    def extract_node_edge_from_json(self, line):
        try:
            if line["remote_addr"] in ENV.server_names:
                node_1 = ENV.server_names[line["remote_addr"]]              # map server names
            else:
                node_1 = line["remote_addr"]
                if node_1 == "-":
                    return None, None, None

            node_2_temp = line["sysloghost"]
            # node_2_temp = line["host"]
            if node_2_temp in ENV.server_names:
                node_2 = ENV.server_names[node_2_temp]                      # map server name
            else:
                node_2 = node_2_temp

            source = self.extract_source_from_user_agent(line["user_agent"])        # extract source service name
            destination = self.extract_destination_from_line(line)                  # extract program name (destination) service name
            method = self.extract_method_from_line(line)                            # extract method name
            edge = {
                "type": "INFO",
                "label": f"{source}_{method}_{destination}",
            }
            if "-" in node_1:                                                       # replace special characters    
                node_1 = f"{node_1}".replace("-", "_")
            if "-" in node_2:
                node_2 = f"{node_2}".replace("-", "_")
            if "." in node_1:
                node_1 = f"IP_{node_1}".replace(".", "_")
            if "." in node_2:
                node_2 = f"IP_{node_2}".replace(".", "_")
        except Exception as e:
            return None, None, None

        for key in line:                                                           # add all other (key,values)
            if "@" not in key and key != "tags":
                edge[key] = line[key]
            if "user_agent" == key:
                try:                                                               # split user agent if ID is present
                    edge["user_agent"], edge["user_agent_id"] = line[key].split(
                        " ")
                except Exception as e:
                    edge[key] = line[key]
        return node_1, node_2, edge
