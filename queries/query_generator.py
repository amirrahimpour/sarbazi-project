from re import search as regex_search
import sys

class QueryGenerator:
    """this class generates custom queries for Neo4j"""

    def __init__(self) -> None:
        self.mapper = {
            "proxy": "P",
            "account": "A",
            "container": "C",
            "object": "O",
            "swift": "S",
            "python-swiftclient-3.5.0": "S",
            "none": "none",
        }
        self.services = ["P", "A", "C", "O", "S"]
        self.error_status = {
            100: ("Continue", ""),
            200: ("OK", ""),
            201: ("Created", ""),
            202: ("Accepted", "The request is accepted for processing."),
            204: ("No Content", ""),
            206: ("Partial Content", ""),
            301: ("Moved Permanently", "The resource has moved permanently."),
            302: ("Found", "The resource has moved temporarily."),
            303: (
                "See Other",
                "The response to the request can be found under a " "different URI.",
            ),
            304: ("Not Modified", ""),
            307: ("Temporary Redirect", "The resource has moved temporarily."),
            400: (
                "Bad Request",
                "The server could not comply with the request since "
                "it is either malformed or otherwise incorrect.",
            ),
            401: (
                "Unauthorized",
                "This server could not verify that you are "
                "authorized to access the document you requested.",
            ),
            402: ("Payment Required", "Access was denied for financial reasons."),
            403: ("Forbidden", "Access was denied to this resource."),
            404: ("Not Found", "The resource could not be found."),
            405: (
                "Method Not Allowed",
                "The method is not allowed for this " "resource.",
            ),
            406: (
                "Not Acceptable",
                "The resource is not available in a format "
                "acceptable to your browser.",
            ),
            408: (
                "Request Timeout",
                "The server has waited too long for the request "
                "to be sent by the client.",
            ),
            409: (
                "Conflict",
                "There was a conflict when trying to complete " "your request.",
            ),
            410: ("Gone", "This resource is no longer available."),
            411: ("Length Required", "Content-Length header required."),
            412: (
                "Precondition Failed",
                "A precondition for this request was not " "met.",
            ),
            413: (
                "Request Entity Too Large",
                "The body of your request was too " "large for this server.",
            ),
            414: (
                "Request URI Too Long",
                "The request URI was too long for this " "server.",
            ),
            415: (
                "Unsupported Media Type",
                "The request media type is not " "supported by this server.",
            ),
            416: (
                "Requested Range Not Satisfiable",
                "The Range requested is not " "available.",
            ),
            417: ("Expectation Failed", "Expectation failed."),
            422: (
                "Unprocessable Entity",
                "Unable to process the contained " "instructions",
            ),
            499: ("Client Disconnect", "The client was disconnected during request."),
            500: (
                "Internal Error",
                "The server has either erred or is incapable of "
                "performing the requested operation.",
            ),
            501: (
                "Not Implemented",
                "The requested method is not implemented by " "this server.",
            ),
            502: ("Bad Gateway", "Bad gateway."),
            503: (
                "Service Unavailable",
                "The server is currently unavailable. "
                "Please try again at a later time.",
            ),
            504: (
                "Gateway Timeout",
                "A timeout has occurred speaking to a " "backend server.",
            ),
            507: (
                "Insufficient Storage",
                "There was not enough space to save the " "resource. Drive: %(drive)s",
            ),
        }
    
    def generate_key_value_query(self, params, draw_graph=True):
        """
        generate query based on key,value (interval) groups given in params
        
        """

        equality_string = ""
        interval_string = "WHERE"
        for i, key_value in enumerate(params):
            key, value = key_value.split("=")
            if "[" in value:
                pattern_found = regex_search(r"\[.*\,.*\]", value)
                if pattern_found:
                    # print(pattern_found, key_value)
                    int1 = value.split("[")[1].split(",")[0]
                    int2 = value.split(",")[1].split("]")[0]
                    if len(interval_string) > len("WHERE"):
                        interval_string += f"and r.{key} >= \'{int1}\' and r.{key} < \'{int2}\'"
                    else:
                        interval_string += f" r.{key} >= \'{int1}\' and r.{key} < \'{int2}\'"
            else:
                equality_string += f"{key}: \'{value}\', "
        
        if len(interval_string) == len("WHERE"):
                interval_string = ""
        if draw_graph:
            query = (
                "\n" 
                + "MATCH (n1)-[r{" 
                + equality_string[:-2] 
                + "}]->(n2) " 
                + interval_string 
                + " RETURN  n1, n2, r" 
                + "\n"
            )
        else:
            query = (
                "\n" 
                + "MATCH (n1)-[r{" 
                + equality_string[:-2] 
                + "}]->(n2) " 
                + interval_string 
                + " with n1, n2, COUNT(r) as num " 
                + " return n1.name, n2.name, num" 
                + "\n"
            )
        
        return query


if __name__ == "__main__":
    query_gen = QueryGenerator()
    # print(sys.argv)
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print(
            """
            python3 query_generator.py key1=value1 key2=[value2,value3] etc.
            for getting edges with key1=value1
            and key2 within [value2,value3] interval
            include --graph for graph visual output, otherwise number of edges with given conditions will be shown

            """
        )

    else:
        params = sys.argv[1:]
        if "--graph" in sys.argv:
            draw_graph = True
            params.remove("--graph")
        else:
            draw_graph = False

        print(
            query_gen.generate_key_value_query(
                params=params, draw_graph=draw_graph
            )
        )