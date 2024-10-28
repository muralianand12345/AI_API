import os
import logging
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import ai, auth
from .utils.logger import logger
from .utils.error_handler import AIApiException
from config import Config

app = FastAPI(
    title="AI Chat API",
    description="AI Chat API with JWT Authentication",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.API.allow_origins,
    allow_credentials=Config.API.allow_credentials,
    allow_methods=Config.API.allow_methods,
    allow_headers=Config.API.allow_headers,
)

@app.exception_handler(AIApiException)
async def api_exception_handler(request: Request, exc: AIApiException):
    if logger:
        logger.error(f"API Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(ai.router, prefix="/ai", tags=["AI Chat"])
