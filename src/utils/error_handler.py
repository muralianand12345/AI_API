from fastapi import HTTPException
from .logger import logger


class AIApiException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        if logger:
            logger.error(f"API Exception: {status_code} - {detail}")