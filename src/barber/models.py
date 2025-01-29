from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Barber(Base):
    __tablename__ = "barber"

    id = Column(Integer, primary_key=True, index=True)
    barber_name = Column(String, nullable=False)
    barber_shop_id = Column(Integer, ForeignKey("barber_shop.id"), nullable=False)

    barber_shop = relationship("BarberShop", back_populates="barbers")
    images = relationship("Image", back_populates="barber")

    working_hours = relationship("WorkingHours", back_populates="barber")
