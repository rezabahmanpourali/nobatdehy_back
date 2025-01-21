# from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
# from sqlalchemy.sql import func
# from database import Base
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.hybrid import hybrid_property


# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     target_id = Column(Integer, ForeignKey('barber_shop.id'), nullable=False)
#     rating = Column(Float, nullable=False)
#     comment = Column(Text, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     barber_shop = relationship("BarberShop", back_populates="comments", uselist=False)