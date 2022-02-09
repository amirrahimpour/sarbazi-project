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
