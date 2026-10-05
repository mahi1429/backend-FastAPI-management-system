from passlib.context import CryptContext
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from security.config import settings
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User, UserRole

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#password utils
def pass_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#jwt utils
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
        email = payload.get("user_email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*allowed_roles: UserRole):
    def role_guard(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in {role.value for role in allowed_roles}:
            role_names = ", ".join(role.value for role in allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of these roles is required: {role_names}",
            )
        return current_user

    return role_guard



require_hr = require_roles(UserRole.HR)
require_maintenance_manager = require_roles(UserRole.MAINTENANCE_MANAGER)
require_maintenance_supervisor = require_roles(UserRole.MAINTENANCE_SUPERVISOR)
require_maintenance_operations = require_roles(
    UserRole.MAINTENANCE_MANAGER,
    UserRole.MAINTENANCE_SUPERVISOR,
)
require_equipment_read = require_roles(
    UserRole.MAINTENANCE_MANAGER,
    UserRole.MAINTENANCE_SUPERVISOR,
    UserRole.REGULAR_STAFF,
)