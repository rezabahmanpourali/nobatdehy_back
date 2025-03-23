# src/barber_shop/crud.py

from sqlalchemy.orm import Session, joinedload
from src.barber_shop import models, schemas
from src.hair_models.models import HairModel

from typing import Optional
from src.barber_shop.models import BarberShop,BarberShopType, DayOfWeek
from datetime import time

def create_default_working_hours(db: Session, barber_shop_id: int):
    default_hours = [
        {
            "day_of_week": DayOfWeek.MONDAY,
            "opening_time": time(9, 0),  # 9:00 AM
            "closing_time": time(21, 0),  # 9:00 PM
            "is_closed": False
        },
        {
            "day_of_week": DayOfWeek.TUESDAY,
            "opening_time": time(9, 0),
            "closing_time": time(21, 0),
            "is_closed": False
        },
        {
            "day_of_week": DayOfWeek.WEDNESDAY,
            "opening_time": time(9, 0),
            "closing_time": time(21, 0),
            "is_closed": False
        },
        {
            "day_of_week": DayOfWeek.THURSDAY,
            "opening_time": time(9, 0),
            "closing_time": time(21, 0),
            "is_closed": False
        },
        {
            "day_of_week": DayOfWeek.FRIDAY,
            "opening_time": time(9, 0),
            "closing_time": time(21, 0),
            "is_closed": False
        },
        {
            "day_of_week": DayOfWeek.SATURDAY,
            "opening_time": time(9, 0),
            "closing_time": time(21, 0),
            "is_closed": False
        },
        {
            "day_of_week": DayOfWeek.SUNDAY,
            "opening_time": time(9, 0),
            "closing_time": time(21, 0),
            "is_closed": True
        }
    ]
    
    for hours in default_hours:
        db_working_hours = models.WorkingHours(
            barber_shop_id=barber_shop_id,
            **hours
        )
        db.add(db_working_hours)
    
    db.commit()

def create_barbershop(db: Session, barber_shop: schemas.BarberShopCreateSchema):
    location_data = barber_shop.location
    working_hours_data = barber_shop.working_hours
    db_location = None

    if location_data:
        db_location = models.Location(latitude=location_data.latitude, longitude=location_data.longitude)
        db.add(db_location)
        db.commit()
        db.refresh(db_location)

    db_barbershop = models.BarberShop(
        **barber_shop.dict(exclude={"location", "shop_type", "working_hours"}), 
        shop_type=barber_shop.shop_type, 
        location_id=db_location.id if db_location else None
    )
    db.add(db_barbershop)
    db.commit()
    db.refresh(db_barbershop)

    if working_hours_data:
        for hours in working_hours_data:
            db_working_hours = models.WorkingHours(
                **hours.dict(),
                barber_shop_id=db_barbershop.id
            )
            db.add(db_working_hours)
    else:
        # If no working hours provided, create default ones
        create_default_working_hours(db, db_barbershop.id)
    
    db.commit()
    db.refresh(db_barbershop)
    return db_barbershop


def update_barbershop(db: Session, barber_shop_id: int, barber_shop: schemas.BarberShopCreateSchema):
    try:
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
                        db_location.update_address_from_coordinates()
                else:
                    db_location = models.Location(latitude=value['latitude'], longitude=value['longitude'])
                    db_location.update_address_from_coordinates()
                    db.add(db_location)
                    db.flush()
                    db_barbershop.location_id = db_location.id
            elif key == "working_hours" and value:
                # Delete existing working hours
                db.query(models.WorkingHours).filter(models.WorkingHours.barber_shop_id == barber_shop_id).delete()
                
                # Add new working hours
                for hours in value:
                    # Handle both Pydantic models and dictionaries
                    hours_data = hours.dict() if hasattr(hours, 'dict') else hours
                    db_working_hours = models.WorkingHours(
                        **hours_data,
                        barber_shop_id=barber_shop_id
                    )
                    db.add(db_working_hours)
            else:
                setattr(db_barbershop, key, value)

        db.flush()
        db.commit()
        db.refresh(db_barbershop)
        return db_barbershop
    except Exception as e:
        db.rollback()
        raise e


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

    return query.offset(skip).limit(limit).all()

def get_barbershop_by_id(db: Session, barber_shop_id: int):
    return (
        db.query(models.BarberShop)
        .options(joinedload(models.BarberShop.location))
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
