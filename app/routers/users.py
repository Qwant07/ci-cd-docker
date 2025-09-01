from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from app import models, schemas, db
from passlib.context import CryptContext
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SessionDep = Annotated[AsyncSession, Depends(db.get_db)]

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: SessionDep):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pwd = hash_password(user.password)
    new_user = models.User(username = user.username, hashed_password = hashed_pwd)
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: SessionDep):
    return db.query(models.User).all()