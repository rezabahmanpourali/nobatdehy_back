# src/barber_shop/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from src.barber_shop.enums import BarberShopType
from src.barber_shop import crud
from src.barber_shop.schemas import (
    BarberHairModelCreateSchema,
    BarberHairModelSchema,
    BarberShopCreateSchema,
    BarberShopSchema,
    CommentCreateSchema,
    CommentSchema,
    ImageCreateSchema,
    ImageSchema,
)
from database import get_db

router = APIRouter()

@router.post("/barbershops/", response_model=BarberShopSchema)
def create_barbershop(barber_shop: BarberShopCreateSchema, db: Session = Depends(get_db)):
    return crud.create_barbershop(db=db, barber_shop=barber_shop)

@router.put("/barbershops/{barber_shop_id}", response_model=BarberShopSchema)
def update_barbershop(barber_shop_id: int, barber_shop: BarberShopCreateSchema, db: Session = Depends(get_db)):
    db_barbershop = crud.get_barbershop_by_id(db=db, barber_shop_id=barber_shop_id)
    if not db_barbershop:
        raise HTTPException(status_code=404, detail="BarberShop not found")
    
    updated_barbershop = crud.update_barbershop(
        db=db, barber_shop_id=barber_shop_id, barber_shop=barber_shop
    )
    return updated_barbershop

@router.get("/barbershops/", response_model=List[BarberShopSchema])
def read_barbershops(
    skip: int = 0,
    limit: int = 10,
    shop_type: Optional[BarberShopType] = None,
    db: Session = Depends(get_db),
):
    return crud.get_barbershops(
        db=db, 
        skip=skip, 
        limit=limit, 
        shop_type=shop_type.value if shop_type else None
    )

@router.get("/barbershops/{barber_shop_id}", response_model=BarberShopSchema)
def read_barbershop(barber_shop_id: int, db: Session = Depends(get_db)):
    db_barbershop = crud.get_barbershop_by_id(db=db, barber_shop_id=barber_shop_id)
    if db_barbershop is None:
        raise HTTPException(status_code=404, detail="BarberShop not found")
    return db_barbershop

@router.post("/barbershops/{barber_shop_id}/comments/", response_model=CommentSchema)
def create_comment(barber_shop_id: int, comment: CommentCreateSchema, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, barber_shop_id=barber_shop_id)

@router.get("/barbershops/{barber_shop_id}/comments/", response_model=List[CommentSchema])
def read_comments(barber_shop_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_barbershop(db=db, barber_shop_id=barber_shop_id)

@router.post("/barbershops/{barber_shop_id}/images/", response_model=ImageSchema)
def add_image(barber_shop_id: int, image: ImageCreateSchema, db: Session = Depends(get_db)):
    return crud.add_image_to_barbershop(db=db, barber_shop_id=barber_shop_id, image=image)

@router.get("/barbershops/{barber_shop_id}/images/", response_model=List[ImageSchema])
def read_images(barber_shop_id: int, db: Session = Depends(get_db)):
    return crud.get_images_by_barbershop(db=db, barber_shop_id=barber_shop_id)

@router.post("/barbershops/{barber_shop_id}/hair_models/", response_model=BarberHairModelSchema)
def create_barber_hair_model(barber_shop_id: int, barber_hair_model: BarberHairModelCreateSchema, db: Session = Depends(get_db)):
    if barber_hair_model.barber_shop_id != barber_shop_id:
        raise HTTPException(status_code=400, detail="barber_shop_id in body does not match URL parameter")
    return crud.create_barber_hair_model(db=db, barber_hair_model=barber_hair_model)

@router.get("/barbershops/{barber_shop_id}/hair_models/", response_model=List[BarberHairModelSchema])
def get_barber_hair_models(barber_shop_id: int, db: Session = Depends(get_db)):
    return crud.get_barber_hair_models(db=db, barber_shop_id=barber_shop_id)