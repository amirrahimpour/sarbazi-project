from logging import Formatter, Handler, getLogger
from logging.handlers import RotatingFileHandler
from os import makedirs as os_makedirs
from os import path as os_path

from config import ENV


class LogManager:
    """ defined to handle logging in the program"""

    def __init__(self):
        super(LogManager, self).__init__()

        self.log_level = ENV.Logger_LogLevel
        self.propagate = ENV.Logger_Propagate
        self.filedir = ENV.Logger_FileDir
        self.filename = ENV.Logger_FileName

        self.handler: Handler = None
        self.formatter: Formatter = None

        self.setup_logger()

    def init_logger(self):
        """initialize a logger
        :return: logger obj
        """
        logger = getLogger(f"file_{self.logger_name()}")
        logger.setLevel(self.log_level)
        logger.propagate = False
        return logger

    @staticmethod
    def logger_name() -> str:
        """ get the logger name for this logger class """
        return __name__

    def init_handler(self, **kwargs) -> Handler:
        """init handler for given handler type

        :return: handler obj
        """        
        formatter = kwargs.get("formatter", True)

        handler = self.log_handler("file")
        handler.setLevel("INFO")

        if formatter:
            formatter = self.log_formatter()
            # handler.setFormatter(formatter)

        return handler

    def log_handler(self, handler_type: str) -> Handler:
        """make log handler obj for given handler type from logging Handler class
        :params(required) handler_type: handler type, file or elastic for now
        :return: handler obj
        """
        if not os_path.exists(f"{ENV.File_ROOT_PATH}/{self.filedir}"):
            os_makedirs(f"{ENV.File_ROOT_PATH}/{self.filedir}")

        self.handler = RotatingFileHandler(
            f"{ENV.File_ROOT_PATH}/{self.filedir}/{self.filename}",
            maxBytes=ENV.File_MAX_SIZE,
            backupCount=ENV.File_BACKUP_COUNT,
        )
        return self.handler

    def log_formatter(self) -> Formatter:
        """make log formatter for given handler type
        :return: log formatter
        """
        formatter = Formatter(
            """{"created_at": "%(asctime)s", "level_name": "%(levelname)s", "module_name": "%(module)s", "status": 
            "%(status)s", "data": %(data)s, "description": "%(message)s", "options": %(options)s}""",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        return formatter

    def setup_logger(self):
        self.f_logger = self.init_logger()
        handler = self.init_handler()
        self.f_logger.addHandler(handler)

    @property
    def file_logger(self):
        """file logger
        :return: logger obj with file handler only
        """
        return self.f_logger

    def info(self, *args, **kwargs):
        self.f_logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.f_logger.error(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.f_logger.warning(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.f_logger.critical(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.f_logger.debug(*args, **kwargs)
