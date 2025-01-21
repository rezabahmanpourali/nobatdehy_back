from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.hair_models.schemas import HairModelCreateSchema, HairModelSchema
from src.hair_models.crud import create_new_hair_model, get_all_hair_models, get_hair_model_by_id
from typing import List
from sqlalchemy.orm import joinedload


router = APIRouter(prefix="/barber-hair-models", tags=["Barber Hair Models"])

@router.post("/hair_model/barber-hair-models/hair_models/", response_model=HairModelSchema)
def create_hair_model_route(hair_model: HairModelCreateSchema, db: Session = Depends(get_db)):
    return create_new_hair_model(db=db, hair_model=hair_model)



@router.get("/hair_models", response_model=List[HairModelSchema])
def read_all_hair_models(db: Session = Depends(get_db)):
    hair_models = get_all_hair_models(db)
    return hair_models


@router.get("/hair_models/{hair_model_id}", response_model=HairModelSchema)
def read_hair_model(hair_model_id: int, db: Session = Depends(get_db)):
    db_hair_model = get_hair_model_by_id(db=db, hair_model_id=hair_model_id)
    if db_hair_model is None:
        raise HTTPException(status_code=404, detail="HairModel not found")
    return db_hair_model