from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from src.comments.schemas import CommentCreate, CommentInDB, CommentUpdate
from src.comments.crud import create_comment, get_comment_by_id, get_comments_for_target, update_comment, delete_comment

router = APIRouter()


@router.post("/", response_model=CommentInDB)
def create_new_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, comment)


@router.get("/{comment_id}", response_model=CommentInDB)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment_by_id(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.get("/target/{target_id}/{target_type}", response_model=List[CommentInDB])
def read_comments_for_target(
    target_id: int, target_type: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    if target_type not in ["Barber", "BarberShop"]:
        raise HTTPException(status_code=400, detail="Invalid target type")
    return get_comments_for_target(db, target_id, target_type, skip=skip, limit=limit)


@router.put("/{comment_id}", response_model=CommentInDB)
def update_existing_comment(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db)):
    updated_comment = update_comment(db, comment_id, comment_update)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment


@router.delete("/{comment_id}", response_model=CommentInDB)
def delete_existing_comment(comment_id: int, db: Session = Depends(get_db)):
    deleted_comment = delete_comment(db, comment_id)
    if not deleted_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return deleted_comment