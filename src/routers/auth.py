from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.error_handler import AIApiException
from ..utils.database import get_db, DBUser
from ..utils.models import UserLogin
from ..utils.auth import create_user, get_user, get_current_user
from ..utils.logger import logger

router = APIRouter()


@router.post(
    "/register", summary="Register new user", description="Register a new user"
)
async def register(user: UserLogin, db: Session = Depends(get_db)):
    try:
        if get_user(db, user.username):
            if logger:
                logger.error(f"Username {user.username} already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        db_user = create_user(db, user.username, user.password)
        if logger:
            logger.info(f"User {db_user.username} registered successfully")
        return {"message": "User registered successfully"}
    except Exception as e:
        if logger:
            logger.error(f"Error registering user '/register': {e}")
        raise AIApiException(detail=str(e))


@router.get("/me")
async def read_users_me(current_user: DBUser = Depends(get_current_user)):
    try:  
        return {
            "username": current_user.susername,
            "created_at": current_user.created_at,
            "last_login": current_user.last_login,
        }
    except Exception as e:
        if logger:
            logger.error(f"Error reading user '/me': {e}")
        raise AIApiException(detail=str(e))
