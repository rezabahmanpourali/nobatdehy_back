from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# مدل مشتریان
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, nullable=False)
    lastn = Column(Text, nullable=False)
    phone = Column(String, nullable=False)
    face_form  = Column(Text,nullable=True)
    hair_form=Column(Text,nullable=True)
    ryecolor=Column(Text,nullable=True)
    like_hair=Column(Text,nullable=True)
    password=Column(Text,nullable=True)
    addresses = relationship("Address", back_populates="customer")

# مدل آدرس‌ها
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    latitude = Column(Text, nullable=False)
    longitude=Column(Text,nullable=True)

    # ارتباط با مدل Customer
    
    customer = relationship("Customer", back_populates="addresses")
