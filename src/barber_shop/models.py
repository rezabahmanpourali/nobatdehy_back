# src/barber_shop/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from src.barber_shop.enums import BarberShopType


class BarberShop(Base):
    __tablename__ = "barber_shop"

    id = Column(Integer, primary_key=True, index=True)
    barber_shop_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    barbers_detail = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    location_id = Column(Integer, ForeignKey("location.id"), nullable=True)
    location = relationship("Location", back_populates="barber_shops")

    barbers = relationship("Barber", back_populates="barber_shop")
    images = relationship("Image", back_populates="barber_shop")
    hair_model_relations = relationship(
        "BarberHairModel", back_populates="barber_shop")
    comments = relationship("Comment", back_populates="barber_shop")
    working_hours = relationship("WorkingHours", back_populates="barber_shop")

    shop_type = Column(Enum(BarberShopType), nullable=True)

