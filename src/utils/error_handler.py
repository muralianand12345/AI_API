from fastapi import HTTPException, status
from typing import Any, Dict
from pydantic import ValidationError


class AIApiException(HTTPException):
    def __init__(self, status_code: int, detail: str, headers: Dict[str, Any] = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def handle_ai_error(error: Exception) -> AIApiException:
    if isinstance(error, ValidationError):
        return AIApiException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        )

    return AIApiException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An error occurred while processing your request",
    )
