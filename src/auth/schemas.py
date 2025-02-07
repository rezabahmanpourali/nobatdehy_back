from pydantic import BaseModel
from typing import Optional,List

class CustomerBase(BaseModel):
    name:  Optional[str] = None
    lastn:  Optional[str] = None
    phone: str
    face_form: Optional[str] = None  # این فیلد اختیاری شد
    hair_form: Optional[str] = None  # این فیلد اختیاری شد
    ryecolor: Optional[str] = None  # این فیلد اختیاری شد
    like_hair: Optional[str] = None  # این فیلد اختیاری شد
    password:  Optional[str] = None

class CustomerOtp(BaseModel):
    phone:str
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
class CustomerWithAddressesResponse(BaseModel):
    customer: CustomerResponse
    addresses: List[AddressResponse] = []