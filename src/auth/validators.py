import re
from typing import Optional
from pydantic import BaseModel, validator, Field
from .config import PHONE_REGEX, LATITUDE_RANGE, LONGITUDE_RANGE, ERROR_MESSAGES

class PhoneNumber(BaseModel):
    phone: str

    @validator('phone')
    def validate_phone(cls, v):
        if not re.match(PHONE_REGEX, v):
            raise ValueError(ERROR_MESSAGES["invalid_phone"])
        return v

class AddressValidator(BaseModel):
    latitude: float
    longitude: float

    @validator('latitude')
    def validate_latitude(cls, v):
        if not LATITUDE_RANGE[0] <= v <= LATITUDE_RANGE[1]:
            raise ValueError(ERROR_MESSAGES["invalid_address"])
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not LONGITUDE_RANGE[0] <= v <= LONGITUDE_RANGE[1]:
            raise ValueError(ERROR_MESSAGES["invalid_address"])
        return v

class CustomerUpdateValidator(BaseModel):
    name: Optional[str] = None
    lastn: Optional[str] = None
    face_form: Optional[str] = None
    hair_form: Optional[str] = None
    ryecolor: Optional[str] = None
    like_hair: Optional[str] = None
    password: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if v and len(v) < 8:
            raise ValueError("رمز عبور باید حداقل ۸ کاراکتر باشد")
        return v 