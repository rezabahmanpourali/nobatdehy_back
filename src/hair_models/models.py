from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class HairModel(Base):
    __tablename__ = "hair_model"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) 

    images = relationship("Image", back_populates="hair_model") 
    barber_relations = relationship("BarberHairModel", back_populates="hair_model")