from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordRequestForm

from database.db import get_db
from models.user import User
from security.utils import create_access_token, verify_password

router = APIRouter(
    prefix= "/auth",
    tags=['auth']
)
@router.post("/login")
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == user_data.username).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail= "database error while fetching user.")

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail = "invalid credentials", headers = {"WWW-Authenticate": "Bearer"})

    try:
        access_token = create_access_token(data = {"user_email" :user.email})
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail = "error while generating access token")

    return {"access_token": access_token, "token_type": "bearer" }
