from pydantic import BaseModel
from typing import Optional, List
from src.images.schemas import ImageRead

class BarberCreate(BaseModel):
    barber_name: str
    barber_shop_id: int

class BarberUpdate(BaseModel):
    barber_name: Optional[str] = None
    barber_shop_id: Optional[int] = None

    class Config:
        orm_mode = True


class BarberInDB(BaseModel):
    id: int
    barber_name: str
    barber_shop_id: int
    images: List[ImageRead] = []  
    class Config:
        orm_mode = True


class ImageInDB(BaseModel):
    id: int
    file_name: str
    url: str

    class Config:
        orm_mode = True