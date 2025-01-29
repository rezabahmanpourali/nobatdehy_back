import sys
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.barber_shop.models import BarberShop
from src.barber.models import Barber
from src.working_hours.models import WorkingHours
from src.working_hours.schemas import WorkingHoursCreate, WorkingHoursUpdate, Barber as BarberSchema, BarberShop as BarberShopSchema

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

router = APIRouter()

@router.post("/working_hours/")
def create_working_hours(working_hours: WorkingHoursCreate, db: Session = Depends(get_db)):
    db_working_hours = WorkingHours(**working_hours.dict())
    db.add(db_working_hours)
    db.commit()
    db.refresh(db_working_hours)
    return db_working_hours

@router.get("/working_hours/{working_hours_id}")
def read_working_hours(working_hours_id: int, db: Session = Depends(get_db)):
    return db.query(WorkingHours).filter(WorkingHours.id == working_hours_id).first()

@router.put("/working_hours/{working_hours_id}")
def update_working_hours(working_hours_id: int, working_hours: WorkingHoursUpdate, db: Session = Depends(get_db)):
    db_working_hours = db.query(WorkingHours).filter(WorkingHours.id == working_hours_id).first()
    if db_working_hours:
        for key, value in working_hours.dict().items():
            setattr(db_working_hours, key, value)
        db.commit()
        db.refresh(db_working_hours)
    return db_working_hours

@router.delete("/working_hours/{working_hours_id}")
def delete_working_hours(working_hours_id: int, db: Session = Depends(get_db)):
    db_working_hours = db.query(WorkingHours).filter(WorkingHours.id == working_hours_id).first()
    if db_working_hours:
        db.delete(db_working_hours)
        db.commit()
    return {"detail": "Working hours deleted"}

@router.get("/working_hours/barber/{barber_id}")
def get_barber_working_hours(barber_id: int, db: Session = Depends(get_db)):
    barber = db.query(Barber).filter(Barber.id == barber_id).first()
    if not barber:
        raise HTTPException(status_code=404, detail="Barber not found")

    working_hours = db.query(WorkingHours).filter(WorkingHours.barber_id == barber_id).all()
    return {
        "barber_id": barber.id,
        "name": barber.name,
        "working_hours": [{"day_of_week": wh.day_of_week, "start_time": wh.start_time, "end_time": wh.end_time} for wh in working_hours]
    }

@router.get("/working_hours/shop/{shop_id}")
def get_shop_working_hours(shop_id: int, db: Session = Depends(get_db)):
    shop = db.query(BarberShop).filter(BarberShop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    working_hours = db.query(WorkingHours).filter(WorkingHours.shop_id == shop_id).all()
    return {
        "shop_id": shop.id,
        "name": shop.name,
        "working_hours": [{"day_of_week": wh.day_of_week, "start_time": wh.start_time, "end_time": wh.end_time} for wh in working_hours]
    }
