from pydantic import BaseModel
from typing import Union

class User(BaseModel):
    username: str
    disabled: Union[bool, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UserInDB(User):
    hashed_password: str