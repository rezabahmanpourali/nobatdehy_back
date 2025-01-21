from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)

    images = relationship("Image", back_populates="category")
    barber_hair_models = relationship("BarberHairModel", back_populates="category")