from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class RequestBody(BaseModel):
    destination_server: str
    program_name: str
    client_ip: str
    remote_addr: str
    date_time: datetime
    time_stamp: datetime
    method: str
    path: str
    protocol: str
    status_int: str
    referer: str
    user_agent: str
    auth_token: str
    bytes_recvd: int
    bytes_sent: int
    client_etag: str
    transaction_id: str
    headers: str
    request_time: float
    source: str
    log_info: str
    request_start_time: datetime
    request_end_time: datetime
    policy_index: int
    source_service: str
    message: str


class Severity(str, Enum):
    err = 'error'
    debug = 'debug'
    info = 'info'
    notice = 'notice'
    warning = 'warning'

class RequestMethods(str, Enum):
    DELETE = "DELETE" 
    GET = "GET" 
    HEAD = "HEAD" 
    POST = "POST" 
    PUT = "PUT" 

