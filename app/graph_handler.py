"""
    this file contains methods for creating graph edges and nodes
"""
from re import search as regex_search
from datetime import datetime

class GraphHandler:
    """
    graph handler class for creating graph
    """

    def __init__(self, neo, parser, logger, env) -> None:
        self.neo = neo  # Neo4j Driver
        self.nodes = []  # graph node names to avoid repeatition
        self.edges = {}  # graph edge names (obsolete)
        self.parser = parser  # log parser object
        self.logger = logger  # logger object (for unprocessible lines)
        self.ENV = env

    def create_graph_txt(self, lines, reset=True):
        """
        create a graph based on input log lings
        """
        if reset:
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

    def create_graph_json(self, lines, reset=True):
        """ create graph from json (list of dict objs)"""
        if reset:
            self.neo.clear_graph()
        for i, _line in enumerate(lines):
            result = self.extract_node_edge_from_json(_line)
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

    def extract_node_edge_from_log(self, line):
        """
        extract nodes and edges from log lines
        """
        try:
            parsed_log = self.parser.parse_log(line)
            node_1 = parsed_log["remote_addr"]
            node_2 = parsed_log["destination_server"]
            source, method, destination = self.get_source_destination(
                parsed_log)
            edge_label = f"{source}_{method}_{destination}"

        except Exception as e:
            self.logger.error(line)
            # print(f"error: {e}, log line: {line}")
            return None, None, None

        try:
            if node_1 == "-" or node_2 == "-":
                return None, None, None

            node_1 = node_1.replace("m-", "m_")
            node_2 = node_2.replace("m-", "m_")
            if node_1 in self.ENV.server_names.keys():
                node_1 = self.ENV.server_names[node_1]
            if node_2 in self.ENV.server_names.keys():
                node_2 = self.ENV.server_names[node_2]
            if "." in node_1:
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

        if "STDERR" in line:
            _type = "ERR"
        else:
            _type = "INFO"

        message = parsed_log["message"][0:90].replace("'", "")

        parsed_log["type"] = _type
        parsed_log["label"] = edge_label
        parsed_log["message"] = message

        return node_1, node_2, parsed_log

    def get_source_destination(self, parsed_log):
        """
        map service names to predefined abbreviations
        """
        source = self.ENV.mapping[parsed_log["source_service"]]
        destination = self.ENV.mapping[parsed_log["program_name"]]

        method = parsed_log["method"]
        return source, method, destination

    def extract_source_from_user_agent(self, user_agent):
        source = None
        try:
            if "server" in user_agent:
                source = self.ENV.mapping[user_agent.split("-server")[0]]
            elif "updater" in user_agent:
                source = self.ENV.mapping[user_agent.split("-updater")[0]]
                source += "U"
            else:
                source = "S"
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
            destination = self.ENV.mapping[
                program_name.split("-server")[0]
            ]
        elif "updater" in program_name:
            destination = self.ENV.mapping[
                program_name.split("-updater")[0]
            ]
            destination += "U"
        else:
            destination = "S"
        return destination

    def extract_method_from_line(self, line):
        if "method" in line:
            method = line["method"]
        else:
            for _method in self.ENV.method_names:
                if _method in line["message"]:
                    return _method
        return method

    def extract_node_edge_from_json(self, line):
        try:
            if line["remote_addr"] in self.ENV.server_names:
                node_1 = self.ENV.server_names[line["remote_addr"]]
            else:
                node_1 = line["remote_addr"]
                if node_1 == "-":
                    return None, None, None

            node_2_temp = line["sysloghost"]
            # node_2_temp = line["host"]
            if node_2_temp in self.ENV.server_names:
                node_2 = self.ENV.server_names[node_2_temp]
            else:
                node_2 = node_2_temp

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
        except Exception as e:
            return None, None, None

        for key in line:
            if "@" not in key and key != "tags":
                edge[key] = line[key]
            if "user_agent" == key:
                try:
                    edge["user_agent"], edge["user_agent_id"] = line[key].split(
                        " ")
                except Exception as e:
                    edge[key] = line[key]
            if key == "datetime":
                u1 = regex_search(r"[(0-9)]*\/[(A-z)]*\/[(0-9)]*\/[(0-9)]*\/[(0-9)]*\/[(0-9)]*", line[key])
                if u1:
                    temp_datetime = u1.group()
                    [day, month, year, hour, minute, second] = temp_datetime.split("/")
                    month = datetime.strptime(f"{day}/{month}/{year}", "%d/%b/%Y").month
                
                u2 = regex_search(r"[(0-9)]*\/[(A-z)]*\/[(0-9)]*\:[(0-9)]*\:[(0-9)]*\:[(0-9)]*", line[key])
                if u2:
                    temp_datetime = u2.group()                    
                    [date, hour, minute, second] = temp_datetime.split(":")
                    [day, month, year] = date.split("/")
                    month = datetime.strptime(date, "%d/%b/%Y").month
                
                edge[key] = f"{year}-{month}-{day}T{hour}:{minute}:{second}"

        return node_1, node_2, edge

    def delete_old_edges(self, new_gte):
        self.neo.delete_edge(new_gte)
