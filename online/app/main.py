import json
from datetime import datetime, timedelta
from time import sleep

from elastic_connection import ElasticConnection
from config import ENV
from log_filter import LogFilter
from graph_handler import GraphHandler
from neo4j_handler import Neo4jHandler
from log_manager import LogManager


if __name__ == '__main__':
    """ here goes the main application flow"""

    print(f'started application @ {datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}')

    # initialize application assets
    logger = LogManager()
    log_filter = LogFilter()
    neo = Neo4jHandler(ENV.neo4j_credentials)
    graph_handler = GraphHandler(neo, log_filter, logger, ENV)
    
    # create elk connection client, initialize time interval values & read logs
    elastic_client = ElasticConnection(ENV.els_config)    
    lte = datetime.now()
    gte = lte - ENV.time_window     
    elastic_client.read_main_log(
        gte=gte.strftime("%Y-%m-%dT%H:%M:%SZ"),
        lte=lte.strftime("%Y-%m-%dT%H:%M:%SZ")
    )    
    with open("LogDB.json") as f:
        lines = json.loads(f.read())
    
    # create graph from the log lines
    graph_handler.create_graph_json(lines)
    print("finished initial graph")

    # start the loop
    while True:
        # wait for the next time_window & read again
        sleep(ENV.sliding.seconds)
        new_lte = lte + ENV.sliding
        new_gte = gte + ENV.sliding

        elastic_client.read_main_log(
            gte=lte.strftime("%Y-%m-%dT%H:%M:%SZ"),
            lte=new_lte.strftime("%Y-%m-%dT%H:%M:%SZ")
        )

        with open("LogDB.json") as f:
            lines_to_add = json.loads(f.read())
        
        # add new lines to the graph
        print(f"adding records from {lte} to {new_lte}")
        graph_handler.create_graph_json(lines_to_add, reset=False)
        
        # remove older edges
        print(f"deleting records older than {new_gte}")
        graph_handler.delete_old_edges(new_gte.strftime("%Y-%m-%dT%H:%M:%SZ"))
        
        # update the time_window params
        lte = new_lte
        gte = new_gte
