from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional, Annotated

class UserBase(BaseModel):
    email: EmailStr
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]

class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8)]

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[Annotated[str, StringConstraints(min_length=3, max_length=50)]] = None
    password: Optional[Annotated[str, StringConstraints(min_length=8)]] = None

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str 