"""
    this file contains the filters applied on the swift log lines
"""
from re import search as regex_search


class LogFilter:
    """
    the general log filter class
    """

    def filter(self, line, filter_name):
        """
        extract feature from log line
        """

        if filter_name == "ip":
            return self.contains_ip(line)
        elif filter_name == "port":
            return self.contains_port(line)
        elif filter_name == "service_name":
            return self.contains_service_name(line)
        elif filter_name == "host":
            return self.contains_host(line)
        else:
            raise Exception(f"Invalid filter keyword: {filter_name}")

    def contains_ip(self, line):
        """
        extract IP from log line (if present)
        """
        # line = line.decode('utf-8')   # this is for storlet

        def map_ip(_ip):
            """
            map IP values to server names
            """
            ip_mapper = {
                "172.24.1.194": "m-cloud1",
                "172.24.1.195": "m-cloud2",
                "172.24.1.196": "m-cloud3",
            }
            if _ip in ip_mapper:
                return ip_mapper[_ip]
            elif _ip != "0.0.0.0":
                return _ip
            else:
                return None

        ip = None
        u = regex_search(r"http:\/\/.*\:([0-9])*\/", line)
        # look for http://xxx:PORT patterns
        if u:
            url = u.group()
            url = url.split("http://")[1]
            ip = url.split(":")[0]
            port = url.split(":")[1][0:-1]
            return map_ip(ip)
        u = regex_search(r"([0-9])*\.([0-9])*\.([0-9])*\.([0-9])*", line)
        # look for x.x.x.x patterns
        if u:
            ip = u.group()
            return map_ip(ip)

    def contains_port(self, line):
        """
        extract port number from log line
        """
        # line = line.decode('utf-8')   # this is for storlet
        port = None
        u = regex_search(r"\(\'([0-9])*\.([0-9])*\.([0-9])*\.\w+\', ([0-9])*\)", line)
        # (x.x.x.x, PORT)
        if u:
            ip_port = u.group()
            ip = regex_search(r"\'([0-9])*\.([0-9])*\.([0-9])*\.\w+\'", ip_port)
            port = ip_port.split(", ")[1][0:-1]
            return port

        u = regex_search(
            r"http:\/\/([0-9])*\.([0-9])*\.([0-9])*\.([0-9])*\:([0-9])*\/", line
        )
        # http://x.x.x.x:PORT
        if u:
            url = u.group()
            ip, port = url[7:-1].split(":")
            return port

        u = regex_search(r"port'\: ([0-9])*", line)
        if u:
            string = u.group()
            port = string.split(": ")[1]
            return port
        u = regex_search(r"http:\/\/.*\:([0-9])*\/", line)
        if u:
            url = u.group()
            url = url.split("http://")[1]
            ip = url.split(":")[0]
            port = url.split(":")[1][0:-1]
            return port
        u = regex_search(r"\:([0-9])*\/", line)
        if u:
            url = u.group()
            port = url[1:-1]
            return port

    def contains_service_name(self, line) -> str:
        """
        extract service name from log line
        """
        # line = line.decode('utf-8')
        service_name = line.split(" ")[4][:-1]

        return service_name

    def contains_host(self, line):
        """
        extract host name from log line
        """
        # line = line.decode('utf-8')
        host = None
        u = regex_search(r"http://(.*)\:([0-9])*", line)
        if u:
            url = u.group()
            host = url.split("http://")[1].split(":")[0]

        return host

    def parse_log(self, line):
        """
        parse swift log lines, extract all properties
        """
        u = regex_search(r"([a-z])*\-server: ", line)
        if u is None:
            return None

        server = line.split(" ")[3]
        temp = u.group().split("-")[0]
        if temp in ["object", "container", "account"]:
            items = line.split("-server: ")[1].split(" ")
            try:
                return {
                    "destination_server": server,
                    "program_name": temp,
                    "remote_addr": items[0],
                    "datetime": f"{items[3]} {items[4]}"[1:-1],
                    "method": items[5][1:],
                    "path": items[6][:-1],
                    "status_int": items[7],
                    "content_length": items[8],
                    "referer": f"{items[9]} {items[10]}"[1:-1],
                    "transaction_id": items[11][1:-1],
                    "user_agent": f"{items[12]} {items[13]}"[1:-1],
                    "request_time": items[14],
                    "additional_info": items[15][1:-1],
                    "server_pid": items[16],
                    "policy_index": items[17],
                    "source_service": f"{items[12]}".split("-server")[0][1:],
                    "message": "none",
                }
            except Exception as e:
                pass
        if temp in ["proxy"]:
            if "STDERR" in line:
                items = line.split("STDERR: ")[1].split(" ")
                try:
                    return {
                        "destination_server": server,
                        "program_name": f"{temp}",
                        "remote_addr": items[0],
                        "datetime": f"{items[3]} {items[4]}"[1:-1],
                        "method": items[5][1:],
                        "path": items[6],
                        "protocol": items[7][:-1],
                        "status_int": items[8],
                        "transaction_id": items[12][:-1],
                        "source_service": "none",
                        "message": line.split("STDERR: ")[1],
                    }
                except Exception as e:
                    return {
                        "destination_server": server,
                        "program_name": f"{temp}",
                        "remote_addr": self.contains_ip(line.split("STDERR: ")[1]),
                        "method": "none",
                        "message": line.split("STDERR: ")[1],
                        "source_service": "none",
                    }

            else:
                items = line.split("-server: ")[1].split(" ")
                return {
                    "destination_server": server,
                    "program_name": temp,
                    "client_ip": items[0],
                    "remote_addr": items[1],
                    "datetime": items[2],
                    "method": items[3],
                    "path": items[4],
                    "protocol": items[5],
                    "status_int": items[6],
                    "referer": items[7],
                    "user_agent": items[8],
                    "auth_token": items[9],
                    "bytes_recvd": items[10],
                    "bytes_sent": items[11],
                    "client_etag": items[12],
                    "transaction_id": items[13],
                    "headers": items[14],
                    "request_time": items[15],
                    "source": items[16],
                    "log_info": items[17],
                    "start_time": items[18],
                    "end_time": items[19],
                    "policy_index": items[20],
                    "source_service": f"{items[8]}".split("-server")[0],
                    "message": "none",
                }
