from sqlalchemy.orm import Session
from src.auth.model import Customer, Address,OtpStore
from src.auth.schemas import CustomerCreate, CustomerUpdate, AddressCreate,AddressResponse,CustomerOtp,CustomerResponse,CustomerUpdate
from src.auth import otp
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException
import jwt
from jwt import ExpiredSignatureError, DecodeError
from jwt.exceptions import InvalidTokenError
from typing import Optional, Tuple, List
from jose import JWTError
from passlib.context import CryptContext
from . import model, schemas
from .config import (
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS, OTP_EXPIRE_MINUTES,
    MAX_OTP_ATTEMPTS, OTP_RESEND_TIMEOUT_MINUTES
)
from .cache import cache
from .logger import logger, AuthException
from .validators import PhoneNumber, AddressValidator, CustomerUpdateValidator
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """تایید رمز عبور"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """هش کردن رمز عبور"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """ایجاد توکن دسترسی"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """ایجاد توکن تجدید"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """تایید توکن"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_and_store_otp(phone: str, db: Session) -> str:
    """تولید و ذخیره OTP"""
    # اعتبارسنجی شماره موبایل
    PhoneNumber(phone=phone)
    
    # بررسی محدودیت تعداد تلاش
    cache_key = f"otp_attempts_{phone}"
    attempts = cache.get(cache_key) or 0
    if attempts >= MAX_OTP_ATTEMPTS:
        raise AuthException(
            status_code=429,
            detail="تعداد تلاش‌های مجاز برای ارسال کد تایید به پایان رسیده است",
            error_code="max_otp_attempts"
        )
    
    # بررسی زمان انتظار برای ارسال مجدد
    resend_key = f"otp_resend_{phone}"
    if cache.get(resend_key):
        raise AuthException(
            status_code=429,
            detail="لطفاً کمی صبر کنید و دوباره تلاش کنید",
            error_code="otp_resend_timeout"
        )
    
    # حذف OTP قبلی اگر وجود داشته باشد
    existing_otp = db.query(model.OtpStore).filter(model.OtpStore.phone == phone).first()
    if existing_otp:
        db.delete(existing_otp)
        db.commit()
    
    # ارسال OTP و دریافت کد تولید شده
    generated_otp = otp.send_otp(phone)
    if not generated_otp:
        raise AuthException(
            status_code=500,
            detail="خطا در ارسال پیامک، لطفاً دوباره تلاش کنید",
            error_code="sms_failed"
        )
    
    # ذخیره OTP در دیتابیس
    otp_store = model.OtpStore(
        phone=phone,
        otp=generated_otp,
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    )
    db.add(otp_store)
    db.commit()
    
    # ذخیره در کش
    cache.set(cache_key, attempts + 1, OTP_RESEND_TIMEOUT_MINUTES * 60)
    cache.set(resend_key, True, OTP_RESEND_TIMEOUT_MINUTES * 60)
    
    return generated_otp

def verify_otp(phone: str, otp: str, db: Session) -> bool:
    """تایید OTP"""
    otp_record = db.query(model.OtpStore).filter(
        model.OtpStore.phone == phone,
        model.OtpStore.otp == otp,
        model.OtpStore.expires_at > datetime.utcnow()
    ).first()
    
    if not otp_record:
        return False
    
    # حذف OTP استفاده شده
    db.delete(otp_record)
    db.commit()
    
    # پاک کردن کش
    cache.delete(f"otp_attempts_{phone}")
    cache.delete(f"otp_resend_{phone}")
    
    return True

def get_customer_phone(db: Session, phone: str) -> Tuple[Optional[model.Customer], List[model.Address]]:
    """دریافت اطلاعات مشتری با شماره موبایل"""
    customer = db.query(model.Customer).filter(model.Customer.phone == phone).first()
    addresses = []
    if customer:
        addresses = db.query(model.Address).filter(model.Address.customer_id == customer.id).all()
    return customer, addresses

def get_customer_id(db: Session, customer_id: int) -> Tuple[Optional[model.Customer], List[model.Address]]:
    """دریافت اطلاعات مشتری با شناسه"""
    customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
    addresses = []
    if customer:
        addresses = db.query(model.Address).filter(model.Address.customer_id == customer_id).all()
    return customer, addresses

def create_customer(db: Session, customer_data: schemas.CustomerCreate) -> model.Customer:
    """ایجاد مشتری جدید"""
    db_customer = model.Customer(**customer_data.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer_data: schemas.CustomerUpdate) -> Optional[model.Customer]:
    """به‌روزرسانی اطلاعات مشتری"""
    db_customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
    if not db_customer:
        return None
    
    # اعتبارسنجی داده‌ها
    validated_data = CustomerUpdateValidator(**customer_data.dict(exclude_unset=True))
    
    for key, value in validated_data.dict(exclude_unset=True).items():
        if key == "password" and value:
            value = get_password_hash(value)
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int) -> bool:
    """حذف مشتری"""
    db_customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
    if not db_customer:
        return False
    
    db.delete(db_customer)
    db.commit()
    return True

def create_address(db: Session, customer_id: int, address_data: schemas.AddressCreate) -> Optional[model.Address]:
    """ایجاد آدرس جدید"""
    # اعتبارسنجی مختصات جغرافیایی
    AddressValidator(**address_data.dict())
    
    db_address = model.Address(**address_data.dict(), customer_id=customer_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session, customer_id: int) -> List[model.Address]:
    """دریافت لیست آدرس‌های مشتری"""
    return db.query(model.Address).filter(model.Address.customer_id == customer_id).all()
