import contextvars
import logging
import sys
import uuid
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn.logging import ColourizedFormatter

from app.config import settings


LOG_DIR = Path("logs")
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

CONSOLE_FMT = "%(asctime)s %(levelprefix)s [%(request_id)s] %(name)s: %(message)s"
CONSOLE_ACCESS_FMT = "%(asctime)s %(levelprefix)s [%(request_id)s] %(message)s"
FILE_FMT = "%(asctime)s [%(levelname)s] [%(request_id)s] %(name)s: %(message)s"
FILE_ACCESS_FMT = "%(asctime)s [%(levelname)s] [%(request_id)s] %(message)s"

_request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = _request_id.get()
        return True


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = str(uuid.uuid4())[:8]
        _request_id.set(rid)
        response = await call_next(request)
        return response


def setup_logging() -> None:
    log_level = logging.INFO # Change as needed
    LOG_DIR.mkdir(exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(ColourizedFormatter(CONSOLE_FMT, DATE_FORMAT))
    console_handler.addFilter(RequestIDFilter())
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_DIR / "app.log")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(FILE_FMT, DATE_FORMAT))
    file_handler.addFilter(RequestIDFilter())
    root_logger.addHandler(file_handler)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).handlers.clear()
        logging.getLogger(name).propagate = True

    if log_level == logging.debug:
        logging.getLogger("sqlalchemy.engine.Engine").setLevel(log_level)


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)
