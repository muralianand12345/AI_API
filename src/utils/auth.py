from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from .database import get_db, DBUser
from .logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if logger:
        logger.info(f"plain_password: {plain_password}")
        logger.info(f"hashed_password: {hashed_password}")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    if logger:
        logger.info(f"password to hash: {password}")
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    if logger:
        logger.info(f"username: {username}")
    return db.query(DBUser).filter(DBUser.username == username).first()


def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = DBUser(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if logger:
        logger.info(f"db_user: {db_user} Saved to database")
    return db_user


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user = get_user(db, credentials.username)
    if not user or not verify_password(credentials.password, user.hashed_password):
        if logger:
            logger.error(f"User {credentials.username} not found or password incorrect")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if logger:
        logger.info(f"User {credentials.username} authenticated")
    return user
