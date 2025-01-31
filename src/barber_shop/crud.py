# src/barber_shop/crud.py

from sqlalchemy.orm import Session, joinedload
from src.barber_shop import models, schemas
from src.hair_models.models import HairModel

from typing import Optional
from src.barber_shop.models import BarberShop,BarberShopType


def create_barbershop(db: Session, barber_shop: schemas.BarberShopCreateSchema):
    location_data = barber_shop.location
    db_location = None

    if location_data:
        db_location = models.Location(latitude=location_data.latitude, longitude=location_data.longitude)
        db.add(db_location)
        db.commit()
        db.refresh(db_location)

    db_barbershop = models.BarberShop(
        **barber_shop.dict(exclude={"location", "shop_type"}), 
        shop_type=barber_shop.shop_type, 
        location_id=db_location.id if db_location else None
    )
    db.add(db_barbershop)
    db.commit()
    db.refresh(db_barbershop)
    return db_barbershop


def update_barbershop(db: Session, barber_shop_id: int, barber_shop: schemas.BarberShopCreateSchema):
    db_barbershop = db.query(models.BarberShop).filter(models.BarberShop.id == barber_shop_id).first()
    
    if not db_barbershop:
        return None

    for key, value in barber_shop.dict(exclude_unset=True).items():
        if key == "location" and value:
            if db_barbershop.location_id:
                db_location = db.query(models.Location).filter(models.Location.id == db_barbershop.location_id).first()
                if db_location:
                    db_location.latitude = value['latitude']
                    db_location.longitude = value['longitude']
            else:
                db_location = models.Location(latitude=value['latitude'], longitude=value['longitude'])
                db.add(db_location)
                db.commit()
                db.refresh(db_location)
                db_barbershop.location_id = db_location.id
        else:
            setattr(db_barbershop, key, value)

    db.commit()
    db.refresh(db_barbershop)
    return db_barbershop


def get_barbershops(
    db: Session,
    skip: int,
    limit: int,
    shop_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    query = db.query(models.BarberShop)
    if shop_type:
        query = query.filter(models.BarberShop.shop_type == models.BarberShopType(shop_type).value)
    
    if min_price is not None or max_price is not None:
        query = query.join(models.BarberHairModel)

        if min_price is not None:
            query = query.filter(models.BarberHairModel.price >= min_price)
        if max_price is not None:
            query = query.filter(models.BarberHairModel.price <= max_price)

        query = query.distinct() 

    datas = query.offset(skip).limit(limit).all()
    for data in datas:
        print(data.price)

    return query.offset(skip).limit(limit).all()

def get_barbershop_by_id(db: Session, barber_shop_id: int):
    return (
        db.query(models.BarberShop)
        .options(joinedload(models.BarbesrShop.location))
        .filter(models.BarberShop.id == barber_shop_id)
        .first()
    )

def create_comment(db: Session, comment: schemas.CommentCreateSchema, barber_shop_id: int):
    db_comment = models.Comment(**comment.dict(), target_id=barber_shop_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_barbershop(db: Session, barber_shop_id: int):
    return db.query(models.Comment).filter(models.Comment.target_id == barber_shop_id).all()

def add_image_to_barbershop(db: Session, barber_shop_id: int, image: schemas.ImageCreateSchema):
    db_image = models.Image(**image.dict(), barber_shop_id=barber_shop_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_images_by_barbershop(db: Session, barber_shop_id: int):
    return db.query(models.Image).filter(models.Image.barber_shop_id == barber_shop_id).all()


def create_barber_hair_model(db: Session, barber_hair_model: schemas.BarberHairModelCreateSchema):
    db_barber_hair_model = models.BarberHairModel(**barber_hair_model.dict())
    db.add(db_barber_hair_model)
    db.commit()
    db.refresh(db_barber_hair_model)
    return db_barber_hair_model


def get_barber_hair_models(db: Session, barber_shop_id: int):
    return (
        db.query(models.BarberHairModel)
        .options(
            joinedload(models.BarberHairModel.category),
            joinedload(models.BarberHairModel.hair_model).joinedload(HairModel.images)
        )
        .filter(models.BarberHairModel.barber_shop_id == barber_shop_id)
        .all()
    )
