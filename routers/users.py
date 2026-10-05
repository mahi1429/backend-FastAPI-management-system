from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.db import get_db
from models.user import User
from models.department import Department
from schemas.user import CreateUser, UserResponse
from security.utils import pass_hash, require_hr

router = APIRouter(
    prefix = "/users",
    tags = ['User']
)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    dependencies=[Depends(require_hr)],
)
def create_user(
    user: CreateUser,
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email or username already registered")

    if user.department_id is not None:
        department = db.query(Department).filter(
            Department.id == user.department_id
        ).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    hashed_pwd = pass_hash(user.password)
    new_user = User(email = user.email,
                    username = user.username,
                    password = hashed_pwd,
                    role = user.role.value,
                    department_id = user.department_id)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already registered") from exc
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error while registering user")

    return new_user 


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_hr)],
)
def get_user(user_id: str, db: Session= Depends(get_db)):
    try:
        user = db.query(User).filter(User.id ==user_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="unexpected database error while fetching user")    

    if not user:
        raise HTTPException(status_code = 404, detail="user not found")

    return user
