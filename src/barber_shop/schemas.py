# src/barber_shop/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, time
from src.hair_models.schemas import HairModelSchema
from src.category.schema import CategoryRead
from src.barber_shop.enums import BarberShopType
from src.barber_shop.models import DayOfWeek

#comment v image
class CommentBaseSchema(BaseModel):
    # user_id: int
    rating: float
    comment: str
    created_at: Optional[datetime] = None

class CommentCreateSchema(CommentBaseSchema):
    pass

class CommentSchema(CommentBaseSchema):
    id: int
    target_id: int

    class Config:
        from_attributes = True
class ImageBaseSchema(BaseModel):
    file_name: str
    url: str

class ImageCreateSchema(ImageBaseSchema):
    pass

class ImageSchema(ImageBaseSchema):
    id: int

    class Config:
        from_attributes = True



#model mo 
class BarberHairModelBaseSchema(BaseModel):
    barber_shop_id: int
    hair_model_id: int
    price: float
    discount_percentage: Optional[float] = 0.0
    category_id: int 

class BarberHairModelCreateSchema(BaseModel):
    barber_shop_id: int
    hair_model_id: int
    price: float
    discount_percentage: Optional[float] = 0.0
    category_id: int

class BarberHairModelSchema(BaseModel):
    id: int
    barber_shop_id: int
    hair_model_id: int
    price: float
    discount_percentage: Optional[float] = 0.0
    category_id: int
    category: CategoryRead
    hair_model: HairModelSchema

    class Config:
        from_attributes = True

#lcoation
class LocationBaseSchema(BaseModel):
    latitude: float
    longitude: float

class LocationCreateSchema(LocationBaseSchema):
    pass

class LocationSchema(LocationBaseSchema):
    id: int

    class Config:
        from_attributes = True

class WorkingHoursBase(BaseModel):
    day_of_week: DayOfWeek
    opening_time: time
    closing_time: time
    is_closed: bool = False

class WorkingHoursCreate(WorkingHoursBase):
    pass

class WorkingHours(WorkingHoursBase):
    id: int
    barber_shop_id: int

    class Config:
        from_attributes = True

# barber shoph
class BarberShopBaseSchema(BaseModel):
    barber_shop_name: str
    description: Optional[str] = None
    address: Optional[str] = None
    barbers_detail: Optional[str] = None
    is_active: bool = True
    shop_type: Optional[BarberShopType] = None

class BarberShopCreateSchema(BarberShopBaseSchema):
    location: Optional[LocationCreateSchema] = None
    working_hours: Optional[List[WorkingHoursCreate]] = None

class BarberShopSchema(BarberShopBaseSchema):
    id: int
    comments: List[CommentSchema] = Field(default_factory=list)
    images: List[ImageSchema] = Field(default_factory=list)
    location: Optional[LocationSchema] = None
    working_hours: List[WorkingHours] = Field(default_factory=list)

    class Config:
        from_attributes = True