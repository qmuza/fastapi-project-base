from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, user
from app.dependencies import get_current_user
from app.schemas import HTTPError
from app.utils import error_response
from app.logger import RequestIDMiddleware, get_logger, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    yield

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)

@app.exception_handler(HTTPException)
async def app_exception_handler(request, exc: HTTPException):
    response = error_response(
        HTTPError(
            status_code=exc.status_code,
            detail=exc.detail,
            headers=exc.headers
        ),
        message=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json")
    )

@app.exception_handler(RequestValidationError)
async def app_exception_handler(request, exc: RequestValidationError):
    response = error_response(
        HTTPError(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=[f'{error["msg"]} at {error["loc"]}' for error in exc.errors()]
        ),
        message="Invalid Request"
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump(mode="json")
    )

@app.exception_handler(Exception)
async def app_exception_handler(request, exc: Exception):
    response = error_response(
        HTTPError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.__str__()
        ),
        message=exc.__str__()
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json")
    )

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
