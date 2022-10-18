
import sys
import json


def main(log_file_name):
    from log_filter import LogFilter
    from neo4j_handler import Neo4jHandler
    from graph_handler import GraphHandler
    from log_manager import LogManager

    logger = LogManager()

    credentials = {"uri": "bolt://localhost:7687",
                   "userName": "neo4j", "password": "test"}

    log_filter = LogFilter()
    neo = Neo4jHandler(credentials)

    file_extension = log_file_name.split(".")[1]
    if file_extension == "txt":
        try:
            with open(log_file_name) as f:
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

    graph_handler = GraphHandler(neo, log_filter, logger)
    if file_extension == "txt":
        graph_handler.create_graph_txt(lines)

    if file_extension == "json":
        graph_handler.create_graph_json(lines)

    print("finished")


if __name__ == "__main__":
    main("LogDB_test.json")
    # print(sys.argv)
    log_file_name = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(
                """
                transform logs into Neo4j graphs
                python3 run.py <log_file_name>
                """
            )
        else:
            log_file_name = sys.argv[1]
            main(log_file_name)
    else:
        print(
            """
            please provide log file name
            """
        )
