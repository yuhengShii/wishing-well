from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import User

# 简单的 token -> user_id 内存缓存（生产环境应用 Redis）
token_cache: dict[str, int] = {}


def set_token_user(token: str, user_id: int):
    """保存 token 与用户的映射"""
    token_cache[token] = user_id


def get_user_id_by_token(token: str) -> Optional[int]:
    """根据 token 获取 user_id"""
    return token_cache.get(token)


def clear_token_user(token: str):
    """删除 token"""
    token_cache.pop(token, None)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    依赖：获取当前登录用户
    从请求头 Authorization: Bearer <token> 提取用户
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="未登录，请先授权")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="授权格式错误")

    token = parts[1]
    user_id = get_user_id_by_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="token 无效或已过期")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user
