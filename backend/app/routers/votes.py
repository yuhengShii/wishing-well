from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Wish, Vote, User
from ..core.auth import get_current_user

router = APIRouter(prefix="/wishes", tags=["投票"])


@router.post("/{wish_id}/vote")
def vote_wish(wish_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """对愿望投票，每人每愿望限投一票"""
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")

    existing = (
        db.query(Vote)
        .filter(Vote.wish_id == wish_id, Vote.user_id == current_user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="已经投过票了")

    vote = Vote(wish_id=wish_id, user_id=current_user.id)
    db.add(vote)
    wish.vote_count += 1
    db.commit()
    return {"message": "投票成功", "vote_count": wish.vote_count}


@router.delete("/{wish_id}/vote")
def unvote_wish(wish_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """取消投票"""
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")

    vote = (
        db.query(Vote)
        .filter(Vote.wish_id == wish_id, Vote.user_id == current_user.id)
        .first()
    )
    if not vote:
        raise HTTPException(status_code=400, detail="尚未投过票")

    db.delete(vote)
    wish.vote_count = max(0, wish.vote_count - 1)
    db.commit()
    return {"message": "取消投票成功", "vote_count": wish.vote_count}


@router.get("/{wish_id}/voted")
def check_voted(wish_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """查询当前用户是否已投过票"""
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")

    voted = (
        db.query(Vote)
        .filter(Vote.wish_id == wish_id, Vote.user_id == current_user.id)
        .first()
    ) is not None
    return {"voted": voted, "vote_count": wish.vote_count}
