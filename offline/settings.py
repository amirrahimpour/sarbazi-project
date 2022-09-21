"""    
    this file contains env variables for the logger application
"""

from os import environ


class ENV:
    # Logger
    Logger_LogLevel = str(environ.get("Logger_LogLevel", "INFO"))
    Logger_Propagate = False
    Logger_FileDir = str(environ.get("Logger_FileDir", "logs"))
    Logger_FileName = str(environ.get("Logger_FileName", "unprocessible.log"))
    File_ROOT_PATH = str(environ.get("File_ROOT_PATH", "logs"))
    File_MAX_SIZE = int(environ.get("File_MAX_SIZE", 83886080))
    File_BACKUP_COUNT = int(environ.get("File_BACKUP_COUNT", 5))

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
    server_names = {        
        "172.20.0.1": "IP_172_20_0_1",
        "172.20.0.2": "m1-r1z1s1",
        "172.20.0.3": "m2-r1z1s1",
        "172.20.0.4": "m3-r1z1s1",
        "172.20.0.5": "m4-r1z1s1",
        "172.20.0.6": "m5-r1z1s1",
        "172.20.0.7": "m6-r1z1s1",
        "172.20.0.8": "m7-r1z1s1",
        "172.20.0.9": "m8-r1z1s1",        
    }
    method_names = [
        "GET", "POST", "PUT", "HEAD", "DELETE", "COPY"
    ]
