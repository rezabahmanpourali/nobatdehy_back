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


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_id = Column(Integer, ForeignKey('barber_shop.id'), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    barber_shop = relationship(
        "BarberShop", back_populates="comments", uselist=False)


class BarberHairModel(Base):
    __tablename__ = "barber_hair_model"

    id = Column(Integer, primary_key=True, index=True)
    barber_shop_id = Column(Integer, ForeignKey(
        'barber_shop.id'), nullable=False)
    hair_model_id = Column(Integer, ForeignKey(
        'hair_model.id'), nullable=False)
    price = Column(Float, nullable=False)
    discount_percentage = Column(Float, nullable=True, default=0.0)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    category = relationship("Category", back_populates="barber_hair_models")
    barber_shop = relationship(
        "BarberShop", back_populates="hair_model_relations")
    hair_model = relationship("HairModel", back_populates="barber_relations")


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    barber_shops = relationship("BarberShop", back_populates="location")
