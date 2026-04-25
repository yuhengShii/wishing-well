from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from ..database import get_db
from ..models import Wish
from ..schemas import WishCreate, WishUpdate, WishResponse

router = APIRouter(prefix="/wishes", tags=["愿望"])


@router.post("/", response_model=WishResponse, status_code=status.HTTP_201_CREATED)
def create_wish(wish: WishCreate, db: Session = Depends(get_db)):
    db_wish = Wish(**wish.model_dump())
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    return db_wish


@router.get("/", response_model=List[WishResponse])
def list_wishes(
    category: Optional[str] = None,
    status: Optional[str] = None,
    sort: Optional[str] = Query(default="latest", pattern="^(latest|votes)$"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Wish).filter(Wish.is_deleted == False)
    if category:
        query = query.filter(Wish.category == category)
    if status:
        query = query.filter(Wish.status == status)
    if sort == "votes":
        query = query.order_by(desc(Wish.vote_count))
    else:
        query = query.order_by(desc(Wish.created_at))
    return query.offset(skip).limit(limit).all()


@router.get("/{wish_id}", response_model=WishResponse)
def get_wish(wish_id: int, db: Session = Depends(get_db)):
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")
    return wish


@router.put("/{wish_id}", response_model=WishResponse)
def update_wish(wish_id: int, data: WishUpdate, db: Session = Depends(get_db)):
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(wish, key, value)
    db.commit()
    db.refresh(wish)
    return wish


@router.delete("/{wish_id}")
def delete_wish(wish_id: int, db: Session = Depends(get_db)):
    wish = db.query(Wish).filter(Wish.id == wish_id, Wish.is_deleted == False).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")
    wish.is_deleted = True
    db.commit()
    return {"message": "删除成功"}
