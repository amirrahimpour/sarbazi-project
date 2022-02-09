"""
MATCH 
(n)-[r:S_GET_P{label:"S_GET_P", status_int:"200"}]->(m) 
RETURN  n,m,r, r.status_int
"""
"""
MATCH 
(n)-[r:S_PUT_P{label:"S_PUT_P"}]->(m) 
WHERE r.status_int=~"2.*"
RETURN  n,m, r.status_int
"""




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

    def generate_query(
        self, source_service: str, program_name: str, status: str, method: str
    ) -> str:
        """generate custom query based on input paramters
        :param source: source service
        :param program_name: destination service
        :param status: status code of the operation
        :param method: method name (GET, PUT, etc.)
        """
        assert (
            source_service in self.services
        ), f"invalid source service: {source_service}"
        assert program_name in self.services, f"invalid program name: {program_name}"

        if source_service in self.mapper.keys():
            source_service = self.mapper[source_service]
        if program_name in self.mapper.keys():
            program_name = self.mapper[program_name]

        status_string = f"\"{status}\""
        if "X" in status.upper():
            status_string = f'"{status[0]}.*"'
        elif status == "000":
            status_string = f'".*"'  # return all statuses
        else:
            assert int(status) in self.error_status, f"invald status: {status}"

        query = (
            "MATCH (n)-[r:"
            + f"{source_service}_{method.upper()}_{program_name}"
            + "{label: "
            + f'"{source_service}_{method.upper()}_{program_name}"'
            + "}]->(m) "
            + f" WHERE r.status_int =~ "
            + status_string
            + " RETURN  n,m,r"
        )
        return query


if __name__ == "__main__":
    query_gen = QueryGenerator()
    print(sys.argv)
    if sys.argv[1] == '--help':
        print(
            """
            
            python3 query_generator.py  [input 1] [input 2] [input 3] [input 4]

            input 1): user agent (for example: P for proxy server)
            input 2): method name (for example: PUT, GET)
            input 3): program name (for example: O for object server)
            input 4): status code (for example: 200, 2xx)
            
            example: python3 query_generator.py  P  PUT  O 2xx
            """
        )
    query = query_gen.generate_query(
        sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[2])
    print(query)
