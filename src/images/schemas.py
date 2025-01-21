from pydantic import BaseModel, ConfigDict

class ImageCreate(BaseModel):
    file_name: str
    url: str
    barber_shop_id: int | None = None
    barber_id: int | None = None
    hair_model_id: int | None = None 
    category_id: int | None = None 

class ImageResponse(ImageCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)




class ImageRead(BaseModel):
    id: int
    file_name: str
    url: str

    class Config:
        orm_mode = True