from dataclasses import dataclass
from os import environ
from datetime import datetime, timedelta


class ENV:
    """ main configurations of the application """

    # Neo4j connection credentials
    credentials = {
        "uri": "bolt://localhost:7687",
        "userName": "neo4j",
        "password": "test"
    }

    # server name mappings
    server_names = {
        "172.18.0.2": "m1-r1z1s48",
        "172.18.0.3": "m2-r1z1s48",
        "172.18.0.4": "m3-r1z1s48",
        "172.18.0.5": "m4-r1z1s48",
        "172.18.0.6": "m5-r1z1s48",
        "172.18.0.7": "m6-r1z1s48",
        "172.18.0.8": "m7-r1z1s48",
        "172.18.0.9": "m8-r1z1s48",
    }

    # list of method names
    method_names = [
        "GET", "POST", "PUT", "HEAD", "DELETE", "COPY"
    ]

    # service name mappings
    mapping = {
        "proxy": "P",
        "account": "A",
        "container": "C",
        "object": "O",
        "Swift": "S",
        "python-swiftclient-3.5.0": "S",
        "proxy-server": "P",
        "account-server": "A",
        "object-server": "O",
        "container-server": "C",
        "none": "none",
    }

    # application moving window parameters
    time_window = timedelta(days=0, hours=0, minutes=10)
    sliding = timedelta(days=0, hours=0, minutes=10)
