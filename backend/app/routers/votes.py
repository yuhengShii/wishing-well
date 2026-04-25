from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Wish, Vote

router = APIRouter(prefix="/wishes", tags=["投票"])


def get_client_id(request: Request) -> str:
    """获取客户端标识，优先从请求头获取，未登录状态下使用 IP"""
    return request.headers.get("X-Client-ID", request.client.host)


@router.post("/{wish_id}/vote")
def vote_wish(wish_id: int, request: Request, db: Session = Depends(get_db)):
    """对愿望投票，每人每愿望限投一票"""
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")

    client_id = get_client_id(request)
    existing = (
        db.query(Vote)
        .filter(Vote.wish_id == wish_id, Vote.client_id == client_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="已经投过票了")

    vote = Vote(wish_id=wish_id, client_id=client_id)
    db.add(vote)
    wish.vote_count += 1
    db.commit()
    return {"message": "投票成功", "vote_count": wish.vote_count}


@router.delete("/{wish_id}/vote")
def unvote_wish(wish_id: int, request: Request, db: Session = Depends(get_db)):
    """取消投票"""
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")

    client_id = get_client_id(request)
    vote = (
        db.query(Vote)
        .filter(Vote.wish_id == wish_id, Vote.client_id == client_id)
        .first()
    )
    if not vote:
        raise HTTPException(status_code=400, detail="尚未投过票")

    db.delete(vote)
    wish.vote_count = max(0, wish.vote_count - 1)
    db.commit()
    return {"message": "取消投票成功", "vote_count": wish.vote_count}


@router.get("/{wish_id}/voted")
def check_voted(wish_id: int, request: Request, db: Session = Depends(get_db)):
    """查询当前客户端是否已投过票"""
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")

    client_id = get_client_id(request)
    voted = (
        db.query(Vote)
        .filter(Vote.wish_id == wish_id, Vote.client_id == client_id)
        .first()
    ) is not None
    return {"voted": voted, "vote_count": wish.vote_count}
