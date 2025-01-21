from sqlalchemy.orm import Session
from src.barber.models import Barber
from src.barber.schema import BarberCreate, BarberUpdate
from src.images.models import Image
from sqlalchemy.orm import joinedload


def create_barber(db: Session, barber: BarberCreate):
    db_barber = Barber(
        barber_name=barber.barber_name,
        barber_shop_id=barber.barber_shop_id,
    )
    db.add(db_barber)
    db.commit()
    db.refresh(db_barber)
    return db_barber



def get_barber_by_id(db: Session, barber_id: int):
    return db.query(Barber).options(joinedload(Barber.images)).filter(Barber.id == barber_id).first()



def get_barbers_by_shop_id(db: Session, barber_shop_id: int):
    return db.query(Barber).options(joinedload(Barber.images)).filter(Barber.barber_shop_id == barber_shop_id).all()

def get_all_barbers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Barber).options(joinedload(Barber.images)).offset(skip).limit(limit).all()

def update_barber(db: Session, barber_id: int, barber_update: BarberUpdate):
    db_barber = get_barber_by_id(db, barber_id)
    if not db_barber:
        return None

    update_data = barber_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_barber, key, value)

    db.commit()
    db.refresh(db_barber)
    return db_barber


def delete_barber(db: Session, barber_id: int):
    db_barber = get_barber_by_id(db, barber_id)
    if db_barber:
        db.delete(db_barber)
        db.commit()
    return db_barber


def get_barber_images(db: Session, barber_id: int):
    """Retrieve all images related to a specific barber."""
    barber = get_barber_by_id(db, barber_id)
    if barber:
        return barber.images
    return []