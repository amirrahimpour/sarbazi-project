from elasticsearch import Elasticsearch, helpers
from utility import save_csv, save_json


class ElasticConnection:
    def __init__(self):
        self.user = 'elastic'
        self.password = 'changeme'
        self.index = "hayoola"
        self.elastic_client = Elasticsearch(
            "http://localhost:9200",
            api_key=(self.user, self.password)
        )

    def read_main_log(self, gte, lte):
        print(f"getting log from {gte} to {lte}")
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": gte,
                                    "lte": lte
                                }
                            }
                        },
                        {
                            "match": {
                                "severity": "info"
                            }
                        },
                        {
                            "regexp": {
                                "user_agent.keyword": ".{5,9}-server [0-9]{2,4}|@&~((account|container|object).+)"
                            }
                        },
                        # {
                        #     "match": {
                        #         "user_agent": {
                        #             "query": "object-server container-server account-server proxy-server",
                        #             "operator": "or"
                        #         }
                        #     }
                        # },
                        # {
                        #     "bool": {
                        #         "must_not": {
                        #             "match": {
                        #                 "user_agent": {
                        #                     "query": "container-auditor object-auditor container-replicator object-updater object-replicator container-sync account-auditor container-updater account-replicator",
                        #                     "operator": "or"
                        #                 }
                        #             }
                        #         }
                        #     },
                        # },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match_phrase": {
                                            "programname": "object-server"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "container-server"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "account-server"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "proxy-server"
                                        }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        }
                    ]
                }
            }
        }

        records = self.elastic_client.search(index=self.index, body=body)
        # attribute_names = records['hits']['hits'][0]['_source'].keys()
        attribute_names = ["@timestamp", "programname", "severity", "message"]

        index_reader = helpers.scan(
            client=self.elastic_client,
            scroll='2m',
            query=body,
            index=self.index)

        # save_csv(index_reader, attribute_names)
        save_json(index_reader)

    def read_all_log(self):
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": "2022-05-31T09:00:00.000Z",
                                    "lte": "2022-05-31T10:00:00.000Z"
                                }
                            }
                        },
                        # {
                        #     "match": {
                        #         "severity": "info"
                        #     }
                        # },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match_phrase": {
                                            "programname": "object-server"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "container-server"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "account-server"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "proxy-server"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "container-auditor"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "object-auditor"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "container-replicator"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "object-updater"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "object-replicator"
                                        }
                                    },
                                    # {
                                    #     "match_phrase": {
                                    #         "programname": "container-sync"
                                    #     }
                                    # },
                                    {
                                        "match_phrase": {
                                            "programname": "account-auditor"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "container-updater"
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "programname": "account-replicator"
                                        }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        }
                    ]
                }
            }
        }

        records = self.elastic_client.search(index=self.index, body=body)
        # attribute_names = records['hits']['hits'][0]['_source'].keys()
        attribute_names = ["@timestamp", "programname", "severity", "message"]

        index_reader = helpers.scan(
            client=self.elastic_client,
            scroll='2m',
            query=body,
            index=self.index)

        # save_csv(index_reader, attribute_names)
        save_json(index_reader)
