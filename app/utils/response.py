from typing import Optional, Any
from http import HTTPStatus
from datetime import datetime
from app.schemas.response import ResponseWrapper, HTTPError

def format_server_status(status_code: int) -> str:
    status = HTTPStatus(status_code)
    return f"HTTP {status_code} {status.name.replace('_', ' ')}"

def success_response(
    data: Any,
    message: str = "success",
    status_code: int = 200,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> ResponseWrapper:
    if not start_time:
        start_time = datetime.now()
    if not end_time:
        end_time = datetime.now()
    
    return ResponseWrapper(
        server_code=status_code,
        server_status=format_server_status(status_code),
        message=message,
        data=data,
        start_time=start_time,
        end_time=end_time,
        execute_time=(end_time - start_time).total_seconds() * 1000 # convert ke ms
    )

def error_response(
    error: HTTPError,
    message: str = "error",
    status_code: int = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> ResponseWrapper:
    if not start_time:
        start_time = datetime.now()
    if not end_time:
        end_time = datetime.now()
    if not status_code:
        status_code = error.status_code
    return ResponseWrapper(
        server_code=status_code,
        server_status=format_server_status(status_code),
        message=message,
        error=error,
        data=None,
        start_time=start_time,
        end_time=end_time,
        execute_time=(end_time - start_time).total_seconds() * 1000 # convert ke ms
    )