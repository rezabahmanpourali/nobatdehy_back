from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Time, ForeignKey
from database import Base

class WorkingHours(Base):
    __tablename__ = 'working_hours'

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    barber_id = Column(Integer, ForeignKey('barber.id'))
    shop_id = Column(Integer, ForeignKey('barber_shop.id'))

    barber = relationship("Barber", back_populates="working_hours")
    
    # Specify foreign key in reverse relationship
    shop = relationship("BarberShop", back_populates="working_hours", foreign_keys=[shop_id])