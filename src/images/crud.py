from sqlalchemy.orm import Session
from src.images.models import Image
from src.images.schemas import ImageCreate

# src/images/crud.py

def create_image(db: Session, image_data: ImageCreate):
    db_image = Image(
        file_name=image_data.file_name,
        url=image_data.url,
        barber_shop_id=image_data.barber_shop_id,
        barber_id=image_data.barber_id,
        hair_model_id=image_data.hair_model_id,
        category_id=image_data.category_id,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_images_by_entity(db: Session, barber_shop_id=None, barber_id=None, hair_model_id=None,category_id=None):
    query = db.query(Image)
    if barber_shop_id:
        query = query.filter(Image.barber_shop_id == barber_shop_id)
    if barber_id:
        query = query.filter(Image.barber_id == barber_id)
    if hair_model_id:
        query = query.filter(Image.hair_model_id == hair_model_id)
    if category_id:
        query = query.filter(Image.category_id == category_id)
    return query.all()