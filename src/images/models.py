from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    barber_id = Column(Integer, ForeignKey("barber.id"), nullable=True)
    barber_shop_id = Column(Integer, ForeignKey("barber_shop.id"), nullable=True)
    hair_model_id = Column(Integer, ForeignKey("hair_model.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)

    barber = relationship("Barber", back_populates="images")
    barber_shop = relationship("BarberShop", back_populates="images")
    hair_model = relationship("HairModel", back_populates="images")
    category = relationship("Category", back_populates="images")