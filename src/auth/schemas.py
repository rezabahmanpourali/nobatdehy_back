from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    lastn: str
    phone: str
    face_form: Optional[str] = None  # این فیلد اختیاری شد
    hair_form: Optional[str] = None  # این فیلد اختیاری شد
    ryecolor: Optional[str] = None  # این فیلد اختیاری شد
    like_hair: Optional[str] = None  # این فیلد اختیاری شد
    password: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    class Config:
        from_attributes = True

class AddressBase(BaseModel):
    longitude: str
    latitude: str

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    customer_id: int
    class Config:
        from_attributes = True
