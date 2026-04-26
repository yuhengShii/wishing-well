from datetime import datetime

from pydantic import BaseModel


class WishBase(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    priority: int = 0
    contact: str | None = None


class WishCreate(WishBase):
    pass


class WishUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    priority: int | None = None
    status: str | None = None
    contact: str | None = None


class WishResponse(WishBase):
    id: int
    status: str
    vote_count: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    openid: str
    nickname: str | None = None
    avatar_url: str | None = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login_at: datetime | None = None

    class Config:
        from_attributes = True
