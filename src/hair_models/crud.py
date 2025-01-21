from sqlalchemy.orm import Session
from src.hair_models.models import HairModel
from src.hair_models.schemas import HairModelCreateSchema
from sqlalchemy.orm import joinedload

def create_new_hair_model(db: Session, hair_model: HairModelCreateSchema):
    db_hair_model = HairModel(**hair_model.dict())
    db.add(db_hair_model)
    db.commit()
    db.refresh(db_hair_model)
    return db_hair_model



def get_all_hair_models(db: Session):
    return db.query(HairModel).options(joinedload(HairModel.images)).all()


def get_hair_model_by_id(db: Session, hair_model_id: int):
    return db.query(HairModel).options(joinedload(HairModel.images)).filter(HairModel.id == hair_model_id).first()
