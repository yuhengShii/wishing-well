from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WishBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: int = 0
    contact: Optional[str] = None


class WishCreate(WishBase):
    pass


class WishUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    contact: Optional[str] = None


class WishResponse(WishBase):
    id: int
    status: str
    vote_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    openid: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True
