from typing import Optional, TypeVar, Generic, Any, Mapping
from datetime import datetime
from pydantic import BaseModel

T = TypeVar("T")

class HTTPError(BaseModel):
    status_code: int
    detail: Any = None
    headers: Optional[Mapping[str, str]] = None

class ResponseWrapper(BaseModel, Generic[T]):
    server_code: int
    server_status: str
    message: str
    error: Optional[HTTPError] = None
    data: Optional[T] = None
    start_time: datetime
    end_time: datetime
    execute_time: float