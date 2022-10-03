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

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})

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

@app.get("/query")
async def generate_query(
    referer: str = Query(
        default=None, 
        description="\*value\*"
    ),
    request_path: str = Query(
        default=None, 
        description="request path",
    ),
    message: str = None,
    programname: str = None,
    severity: Severity = None,
    sysloghost: str = None,    
    transaction_id: str = None,    
    server_pid: int = None,
    request_time: float = None,
    port: int = Query(
        default=None, 
        ge=0, le=65536        
    ),
    remote_addr: str = None,
    datetime: datetime = Query(
        default=None,
        description="correct format: YYYY/mm/ddThh:mm:ss"
    ),
    user_agent: str = None,
    request_method: RequestMethods = None,
    status_int: int = None,
    host: str = None,
    account_path: str = None,
    protocol: float = None,
    source: str = None,
    auth_token: str = None,
    bytes_recvd: int = None,
    client_ip: str = Query(
        default=None,
        description="client IP"    
    ),
    bytes_sent: int = None,
    request_end_time: datetime = None,
    request_start_time: datetime = None,
    client_etag: str = None,    
    container_path: str = None,
    headers: str = None,
    log_info: str = None,
    policy_index: int = None,
    draw_graph: bool = Query(
        default=True, 
        description="Whether the result of query contains graph or not"
    )
):
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
    if server_pid:
        params["server_pid"] = server_pid
    if request_time:
        params["request_time"] = request_time

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
    if status_int:
        params["status_int"] = status_int
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
    if bytes_recvd:
        params["bytes_recvd"] = bytes_recvd

    if client_ip:
        params["client_ip"] = client_ip
    if bytes_sent:
        params["bytes_sent"] = bytes_sent

    if request_end_time:
        params["request_end_time"] = request_end_time
    if request_start_time:
        params["request_start_time"] = request_start_time
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
