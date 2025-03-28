# src/barber_shop/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean, DateTime, Enum, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from src.barber_shop.enums import BarberShopType
from enum import Enum as PyEnum
from src.barber_shop.utils import get_address_from_coordinates

class DayOfWeek(PyEnum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class WorkingHours(Base):
    __tablename__ = "working_hours"

    id = Column(Integer, primary_key=True, index=True)
    barber_shop_id = Column(Integer, ForeignKey("barber_shop.id"), nullable=False)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    is_closed = Column(Boolean, default=False)

    barber_shop = relationship("BarberShop", back_populates="working_hours")

class BarberShop(Base):
    __tablename__ = "barber_shop"

    id = Column(Integer, primary_key=True, index=True)
    barber_shop_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    barbers_detail = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    location_id = Column(Integer, ForeignKey("location.id"), nullable=True) 
    location = relationship("Location", back_populates="barber_shops")

    barbers = relationship("Barber", back_populates="barber_shop")
    images = relationship("Image", back_populates="barber_shop")
    hair_model_relations = relationship("BarberHairModel", back_populates="barber_shop")
    comments = relationship("Comment", back_populates="barber_shop")
    working_hours = relationship("WorkingHours", back_populates="barber_shop", cascade="all, delete-orphan")

    shop_type = Column(Enum(BarberShopType), nullable=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    target_id = Column(Integer, ForeignKey('barber_shop.id'), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    barber_shop = relationship("BarberShop", back_populates="comments", uselist=False)

class BarberHairModel(Base):
    __tablename__ = "barber_hair_model"

    id = Column(Integer, primary_key=True, index=True)
    barber_shop_id = Column(Integer, ForeignKey('barber_shop.id'), nullable=False)
    hair_model_id = Column(Integer, ForeignKey('hair_model.id'), nullable=False)
    price = Column(Float, nullable=False)
    discount_percentage = Column(Float, nullable=True, default=0.0)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False) 

    category = relationship("Category", back_populates="barber_hair_models") 
    barber_shop = relationship("BarberShop", back_populates="hair_model_relations")
    hair_model = relationship("HairModel", back_populates="barber_relations")

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False) 
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)  # آدرس متنی
    city = Column(String, nullable=True)     # شهر
    state = Column(String, nullable=True)    # استان
    postal_code = Column(String, nullable=True)  # کد پستی
    country = Column(String, nullable=True)  # کشور

    barber_shops = relationship("BarberShop", back_populates="location")

    def update_address_from_coordinates(self):
        """
        به‌روزرسانی آدرس متنی با استفاده از مختصات جغرافیایی
        """
        address_data = get_address_from_coordinates(self.latitude, self.longitude)
        if address_data:
            self.address = address_data['address']
            self.city = address_data['city']
            self.state = address_data['state']
            self.postal_code = address_data['postal_code']
            self.country = address_data['country']

            