from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class SMS(Base):
    __tablename__ = "sms"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    body = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False) 