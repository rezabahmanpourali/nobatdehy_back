from sqlalchemy.orm import Session
from src.comments import models, schemas



def create_barbershop(db: Session, barber_shop: schemas.BarberShopCreate):
    db_barbershop = models.BarberShop(**barber_shop.dict())
    db.add(db_barbershop)
    db.commit()
    db.refresh(db_barbershop)
    return db_barbershop


def get_barbershops(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.BarberShop).offset(skip).limit(limit).all()


def get_barbershop_by_id(db: Session, barber_shop_id: int):
    return db.query(models.BarberShop).filter(models.BarberShop.id == barber_shop_id).first()



def create_comment(db: Session, comment: schemas.CommentCreate, barber_shop_id: int):
    db_comment = models.Comment(**comment.dict(), target_id=barber_shop_id, target_type="BarberShop")
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_by_barbershop(db: Session, barber_shop_id: int):
    return db.query(models.Comment).filter(models.Comment.target_id == barber_shop_id).all()