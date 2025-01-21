from pydantic import BaseModel
from typing import List, Optional
from src.images.schemas import ImageRead

class CategoryBase(BaseModel):
    title: Optional[str] = None

class CategoryRead(CategoryBase):
    id: int
    images: List[ImageRead] = []

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass