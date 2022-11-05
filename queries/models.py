from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Severity(str, Enum):
    """ available options for Severity field"""
    err = 'error'
    debug = 'debug'
    info = 'info'
    notice = 'notice'
    warning = 'warning'

class RequestMethods(str, Enum):
    """ available options for RequestMethod field"""
    DELETE = "DELETE" 
    GET = "GET" 
    HEAD = "HEAD" 
    POST = "POST" 
    PUT = "PUT" 

