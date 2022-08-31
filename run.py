import sys
import json
from log_filter import LogFilter
from neo4j_handler import Neo4jHandler
from graph_handler import GraphHandler
from logs.log_manager import LogManager

def main(log_file_name):
    """ main function of the application """
    logger = LogManager()                                           # initialize logger object                    
    credentials = {"uri": "bolt://localhost:7687",
                   "userName": "neo4j", "password": "test"}

    log_filter = LogFilter()                                        # initialize log filter object
    neo = Neo4jHandler(credentials)                                 # initialize neo4j handler object

    file_extension = log_file_name.split(".")[1]                    # extract input file extension
    if file_extension == "txt":
        try:
            with open(log_file_name) as f:                          # split into lines
                lines = f.read().split("\n")
        except FileNotFoundError as e:
            print(f"{e}")
            exit(2)
    if file_extension == "json":
        try:
            with open(log_file_name) as f:
                lines = json.loads(f.read())
        except FileNotFoundError as e:
            print(f"{e}")
            exit(2)

    graph_handler = GraphHandler(neo, log_filter, logger)           # initialize graph handler object
    if file_extension == "txt":
        graph_handler.create_graph_txt(lines)                       # call function for creating graph from .txt file

    if file_extension == "json":
        graph_handler.create_graph_json(lines)                      # call function for creating graph from .json file

    print("finished")


if __name__ == "__main__":
    log_file_name = None
    if len(sys.argv) > 1:                                           # check if input file name is given    
        if sys.argv[1] == "--help":                                 # print the manual if --help is given
            print(
                """
                transform logs into Neo4j graphs
                python3 run.py <log_file_name>
                """
            )
        else:
            log_file_name = sys.argv[1]                             # extract file name from input
            main(log_file_name)
    else:
        print(
            """
            please provide log file name
            """
        )
