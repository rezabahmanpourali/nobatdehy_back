# src/hair_models/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class ImageSchema(BaseModel):
    id: int
    file_name: str
    url: str

    class Config:
        from_attributes = True 

class HairModelBaseSchema(BaseModel):
    name: str 

class HairModelCreateSchema(HairModelBaseSchema):
    pass

class HairModelSchema(HairModelBaseSchema):
    id: int
    images: Optional[List[ImageSchema]] = Field(default_factory=list)

    class Config:
        from_attributes = True