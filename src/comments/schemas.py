from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CommentBase(BaseModel):
    user_id: int
    rating: float
    comment: str
    created_at: Optional[datetime] = None


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    target_id: int 

    class Config:
        orm_mode = True


class BarberShopBase(BaseModel):
    barber_shop_name: str
    barber_shop_image: str
    is_active: bool = True


class BarberShopCreate(BarberShopBase):
    pass


class BarberShop(BarberShopBase):
    id: int
    comments: List[Comment] = [] 

    class Config:
        orm_mode = True