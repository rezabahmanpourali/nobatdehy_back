from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from src.barber.schema import BarberCreate, BarberInDB, BarberUpdate, ImageInDB
from src.barber.crud import create_barber, get_barber_by_id, get_all_barbers, update_barber, delete_barber, get_barber_images, get_barbers_by_shop_id

router = APIRouter()

@router.post("/", response_model=BarberInDB)
def create_new_barber(barber: BarberCreate, db: Session = Depends(get_db)):
    return create_barber(db, barber)


@router.get("/{barber_id}", response_model=BarberInDB)
def read_barber(barber_id: int, db: Session = Depends(get_db)):
    db_barber = get_barber_by_id(db, barber_id)
    if not db_barber:
        raise HTTPException(status_code=404, detail="Barber not found")
    return db_barber


@router.get("/", response_model=List[BarberInDB])
def read_all_barbers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_barbers(db, skip=skip, limit=limit)


@router.put("/{barber_id}", response_model=BarberInDB)
def update_existing_barber(barber_id: int, barber_update: BarberUpdate, db: Session = Depends(get_db)):
    updated_barber = update_barber(db, barber_id, barber_update)
    if not updated_barber:
        raise HTTPException(status_code=404, detail="Barber not found")
    return updated_barber


@router.delete("/{barber_id}", response_model=BarberInDB)
def delete_existing_barber(barber_id: int, db: Session = Depends(get_db)):
    deleted_barber = delete_barber(db, barber_id)
    if not deleted_barber:
        raise HTTPException(status_code=404, detail="Barber not found")
    return deleted_barber


@router.get("/{barber_id}/images", response_model=List[ImageInDB])
def read_barber_images(barber_id: int, db: Session = Depends(get_db)):
    images = get_barber_images(db, barber_id)
    if images is None:
        raise HTTPException(status_code=404, detail="Barber or images not found")
    return images


@router.get("/barbershop/{barber_shop_id}/barbers")
def read_barbers_by_shop(barber_shop_id: int, db: Session = Depends(get_db)):
    barbers = get_barbers_by_shop_id(db, barber_shop_id)
    if not barbers:
        raise HTTPException(status_code=404, detail="No barbers found for this shop")
    return barbers