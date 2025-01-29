from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Time, ForeignKey
from database import Base

metadata = Base.metadata

class WorkingHours(Base):
    __tablename__ = 'working_hours'

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    barber_id = Column(Integer, ForeignKey('barber.id'))
    shop_id = Column(Integer, ForeignKey('barber_shop.id'))

    barber = relationship("Barber", back_populates="working_hours")
    shop = relationship("BarberShop", back_populates="working_hours")

class Barber(Base):
    __tablename__ = 'barber'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    working_hours = relationship("WorkingHours", back_populates="barber")

class BarberShop(Base):
    __tablename__ = 'barber_shop'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    working_hours = relationship("WorkingHours", back_populates="shop")
