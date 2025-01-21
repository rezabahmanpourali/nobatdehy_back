from sqlalchemy.orm import Session
from src.category.models import Category
from src.category.schema import CategoryCreate, CategoryUpdate
from sqlalchemy.orm import joinedload

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).options(joinedload(Category.images)).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).options(joinedload(Category.images)).filter(Category.id == category_id).first()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(title=category.title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False