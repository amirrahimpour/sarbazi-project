from uvicorn import run
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from typing import List, Union, Optional
from models import Severity, RequestMethods
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from query_generator import QueryGenerator

query_gen = QueryGenerator()

app = FastAPI(
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}, 
    title="Neo4j Query Generator",
    description="This webservice is developed to generate Cypher Queries for Neo4j."
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get("/generate")
async def generate_query(
    referer: str = Query(
        default=None, 
        description="\*value\*"
    ),
    request_path: str = Query(
        default=None, 
        description="\*value\*"
    ),
    message: str = Query(
        default=None, 
        description="\*value\*"
    ),
    programname: str = None,
    severity: Severity = None,
    sysloghost: str = None,    
    transaction_id: str = None,
    server_pid_start_val: int = None,
    server_pid_end_val: int = None,
    request_time_start_val: float = None,
    request_time_end_val: float = None,
    port: int = Query(
        default=None, 
        ge=0, le=65535
    ),
    remote_addr: str = None,
    datetime: datetime = Query(
        default=None,
        description="correct format: YYYY-mm-ddThh:mm:ss"
    ),
    user_agent: str = None,
    request_method: RequestMethods = None,
    status_int_start_val: int = None,
    status_int_end_val: int = None,
    host: str = None,
    account_path: str = Query(
        default=None, 
        description="\*value\*"
    ),
    protocol: float = None,
    source: str = None,
    auth_token: str = None,
    bytes_recvd_start_val: int = None,
    bytes_recvd_end_val: int = None,
    client_ip: str = Query(
        default=None
    ),
    bytes_sent_start_val: int = None,
    bytes_sent_end_val: int = None,
    request_end_time_start_val: datetime = Query(
        default=None,
        description="correct format: YYYY-mm-ddThh:mm:ss"
    ),
    request_end_time_end_val: datetime = Query(
        default=None,
        description="correct format: YYYY-mm-ddThh:mm:ss"
    ),
    request_start_time_start_val: datetime = Query(
        default=None,
        description="correct format: YYYY-mm-ddThh:mm:ss"
    ),
    request_start_time_end_val: datetime = Query(
        default=None,
        description="correct format: YYYY-mm-ddThh:mm:ss"
    ),
    client_etag: str = None,    
    container_path: str = Query(
        default=None, 
        description="\*value\*"
    ),
    headers: str = None,
    log_info: str = Query(
        default=None, 
        description="\*value\*"
    ),
    policy_index: int = None,
    draw_graph: bool = Query(
        default=True, 
        description="determine whether the result of query contains graph or not (show table)"
    )
) -> str:
    """
    This method generates cypher query with the given arguments
    """        
    params = {}
    if referer:
        params["referer"] = referer

    if request_path:
        params["request_path"] = request_path
    if message:
        params["message"] = message
    if programname:
        params["programname"] = programname
    if severity:
        params["severity"] = severity
    if sysloghost:
        params["sysloghost"] = sysloghost

    if transaction_id:
        params["transaction_id"] = transaction_id

    if server_pid_start_val or server_pid_end_val:
        if server_pid_start_val and not server_pid_end_val:
            params["server_pid"] = server_pid_start_val
        elif not server_pid_start_val and server_pid_end_val:
            params["server_pid"] = server_pid_end_val
        elif server_pid_start_val and server_pid_end_val:
            params["server_pid"] = f"[{server_pid_start_val},{server_pid_end_val}]"

    if request_time_start_val or request_time_end_val:
        if request_time_start_val and not request_time_end_val:
            params["request_time"] = request_time_start_val
        elif not request_time_start_val and request_time_end_val:
            params["request_time"] = request_time_end_val
        elif request_time_start_val and request_time_end_val:
            params["request_time"] = f"[{request_time_start_val},{request_time_end_val}]"

    if port:
        params["port"] = port
    if remote_addr:
        params["remote_addr"] = remote_addr
    if datetime:
        params["datetime"] = datetime
    if user_agent:
        params["user_agent"] = user_agent
    if request_method:
        params["request_method"] = request_method
    
    if status_int_start_val or status_int_end_val:
        if status_int_start_val and not status_int_end_val:
            params["status_int"] = status_int_start_val
        elif not status_int_start_val and status_int_end_val:
            params["status_int"] = status_int_end_val
        elif status_int_start_val and status_int_end_val:
            params["status_int"] = f"[{status_int_start_val},{status_int_end_val}]"
    
    if host:
        params["host"] = host

    if account_path:
        params["account_path"] = account_path
    if protocol:
        params["protocol"] = protocol
    if source:
        params["source"] = source
    if auth_token:
        params["auth_token"] = auth_token
    if bytes_recvd_start_val or bytes_recvd_end_val:
        if bytes_recvd_start_val and not bytes_recvd_end_val:
            params["bytes_recvd"] = bytes_recvd_start_val
        elif not bytes_recvd_start_val and bytes_recvd_end_val:
            params["bytes_recvd"] = bytes_recvd_end_val
        elif bytes_recvd_start_val and bytes_recvd_end_val:
            params["bytes_recvd"] = f"[{bytes_recvd_start_val},{bytes_recvd_end_val}]"

    if client_ip:
        params["client_ip"] = client_ip
    
    if bytes_sent_start_val or bytes_sent_end_val:
        if bytes_sent_start_val and not bytes_sent_end_val:
            params["bytes_sent"] = bytes_sent_start_val
        elif not bytes_sent_start_val and bytes_sent_end_val:
            params["bytes_sent"] = bytes_sent_end_val
        elif bytes_sent_start_val and bytes_sent_end_val:
            params["bytes_sent"] = f"[{bytes_sent_start_val},{bytes_sent_end_val}]"

    if request_end_time_start_val or request_end_time_end_val:
        if request_end_time_start_val and not request_end_time_end_val:
            params["request_end_time"] = request_end_time_start_val
        elif not request_end_time_start_val and request_end_time_end_val:
            params["request_end_time"] = request_end_time_end_val
        elif request_end_time_start_val or request_end_time_end_val:
            params["request_end_time"] = f"[{request_end_time_start_val},{request_end_time_end_val}]"
            

    if request_start_time_start_val or request_start_time_end_val:
        if request_start_time_start_val and not request_start_time_end_val:
            params["request_start_time"] = request_start_time_start_val
        elif not request_start_time_start_val and request_start_time_end_val:
            params["request_start_time"] = request_start_time_end_val
        elif request_start_time_start_val and request_start_time_end_val:
            params["request_start_time"] = f"[{request_start_time_start_val},{request_start_time_end_val}]"
        
    if client_etag:
        params["client_etag"] = client_etag

    if container_path:
        params["container_path"] = container_path
    if headers:
        params["headers"] = headers
    if log_info:
        params["log_info"] = log_info

    if policy_index:
        params["policy_index"] = policy_index

    params_concat = [f"{key}={params[key]}" for key in params]

    query = query_gen.generate_key_value_query(params_concat, draw_graph)
    return query

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
