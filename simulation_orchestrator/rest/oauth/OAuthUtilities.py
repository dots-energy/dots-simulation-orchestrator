from typing import Annotated, Union, Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from simulation_orchestrator.rest.schemas.user_schemas import UserInDB, TokenData
import datetime

from simulation_orchestrator.io.log import LOGGER

from jose import JWTError, jwt

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
USE_AUTH = True

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/simulation/token", auto_error=False
)

users = {
    "DotsUser": {
        "username": "DotsUser",
        "hashed_password": "hash hash",
        "disabled": False,
    }
}


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    if username in users:
        user_dict = users[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        LOGGER.info("Invalid Username")
        return False
    if not verify_password(password, user.hashed_password):
        LOGGER.info("Invalid Password")
        return False
    return user


def create_access_token(
    data: dict, expires_delta: Union[datetime.timedelta, None] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[Optional[str], Depends(oauth2_scheme)]):
    if not USE_AUTH:
        # bypass auth if configured to disable
        return UserInDB(username="anonymous", hashed_password="", disabled=False)

    if token is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user
