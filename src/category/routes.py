from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.category.schema import CategoryCreate, CategoryUpdate, CategoryRead
from typing import List
from src.category.crud import (
    get_categories,
    get_category,
    create_category,
    update_category,
    delete_category,
)

router = APIRouter()

@router.get("/categories", response_model=List[CategoryRead])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_categories(db, skip=skip, limit=limit)

@router.get("/categories/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/categories", response_model=CategoryRead)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category=category)

@router.put("/categories/{category_id}", response_model=CategoryRead)
def update_existing_category(
    category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)
):
    db_category = update_category(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/categories/{category_id}")
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    if not delete_category(db, category_id=category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}