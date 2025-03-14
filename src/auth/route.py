from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from . import crud
from .schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    AddressCreate, AddressResponse, CustomerWithAddressesResponse
)
from fastapi.security import OAuth2PasswordBearer
from .cache import rate_limiter, cache
from .logger import AuthException, handle_auth_error
from typing import Optional

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/customers/verify/", auto_error=False)

async def get_current_user(
    authorization: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> CustomerWithAddressesResponse:
    """دریافت اطلاعات کاربر فعلی از توکن"""
    if not authorization:
        raise AuthException(
            status_code=401,
            detail="توکن احراز هویت یافت نشد",
            error_code="missing_token"
        )
    
    payload = crud.verify_token(authorization)
    if not payload or payload.get("type") != "access":
        raise AuthException(
            status_code=401,
            detail="توکن نامعتبر یا منقضی شده است",
            error_code="invalid_token"
        )
    
    user_id = payload.get("sub")
    customer, addresses = crud.get_customer_id(db, user_id)
    
    if not customer:
        raise AuthException(
            status_code=404,
            detail="کاربر یافت نشد",
            error_code="user_not_found"
        )
    
    return {"customer": customer, "addresses": addresses}

@router.post("/customers/otp/")
async def send_otp(phone: str, db: Session = Depends(get_db)):
    """ارسال کد تایید"""
    try:
        rate_limiter.is_rate_limited(f"otp_{phone}")
        
        cache_key = f"otp_{phone}"
        if cache.get(cache_key):
            return {"message": "کد تایید قبلاً ارسال شده است"}
        
        otp = crud.generate_and_store_otp(phone, db)
        
        cache.set(cache_key, True, 60)  
        
        return {"message": "کد تایید با موفقیت ارسال شد"}
    except Exception as e:
        return handle_auth_error(e)

@router.post("/customers/verify/")
async def verify_otp(phone: str, otp: str, db: Session = Depends(get_db)):
    """تایید کد تایید و ورود کاربر"""
    try:
        is_valid = crud.verify_otp(phone, otp, db)
        if not is_valid:
            raise AuthException(
                status_code=400,
                detail="کد تایید نامعتبر یا منقضی شده است",
                error_code="invalid_otp"
            )
        
        customer, addresses = crud.get_customer_phone(db, phone)
        
        if customer:
            # کاربر موجود است
            access_token = crud.create_access_token({"sub": str(customer.id)})
            refresh_token = crud.create_refresh_token({"sub": str(customer.id)})
            return {
                "message": "ورود موفقیت‌آمیز",
                "data": {"customer": customer, "addresses": addresses},
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        
        # ایجاد کاربر جدید
        customer_data = CustomerCreate(phone=phone)
        customer = crud.create_customer(db, customer_data)
        access_token = crud.create_access_token({"sub": str(customer.id)})
        refresh_token = crud.create_refresh_token({"sub": str(customer.id)})
        
        return {
            "message": "ثبت‌نام موفقیت‌آمیز",
            "data": customer,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    except Exception as e:
        return handle_auth_error(e)

@router.post("/customers/refresh/")
async def refresh_token(
    authorization: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """تجدید توکن دسترسی"""
    try:
        payload = crud.verify_token(authorization)
        if not payload or payload.get("type") != "refresh":
            raise AuthException(
                status_code=401,
                detail="توکن نامعتبر است",
                error_code="invalid_token"
            )
        
        user_id = payload.get("sub")
        new_access_token = crud.create_access_token({"sub": user_id})
        return {"access_token": new_access_token}
    except Exception as e:
        return handle_auth_error(e)

@router.post("/customers/logout")
async def logout(
    authorization: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """خروج از حساب کاربری"""
    try:
        payload = crud.verify_token(authorization)
        if not payload or payload.get("type") != "refresh":
            raise AuthException(
                status_code=401,
                detail="توکن نامعتبر است",
                error_code="invalid_token"
            )
        
        user_id = payload.get("sub")
        # پاک کردن توکن از کش
        cache.delete(f"refresh_token_{user_id}")
        return {"message": "خروج موفقیت‌آمیز"}
    except Exception as e:
        return handle_auth_error(e)

@router.get("/customers/me/", response_model=CustomerWithAddressesResponse)
async def get_current_user_info(current_user: CustomerWithAddressesResponse = Depends(get_current_user)):
    """دریافت اطلاعات کاربر فعلی"""
    return current_user

@router.put("/customers/edit/", response_model=CustomerResponse)
async def update_customer_info(
    customer_data: CustomerUpdate,
    current_user: CustomerWithAddressesResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """به‌روزرسانی اطلاعات کاربر"""
    try:
        updated_customer = crud.update_customer(
            db,
            current_user["customer"].id,
            customer_data
        )
        if not updated_customer:
            raise AuthException(
                status_code=404,
                detail="کاربر یافت نشد",
                error_code="user_not_found"
            )
        return updated_customer
    except Exception as e:
        return handle_auth_error(e)

@router.delete("/customers/delete/")
async def delete_customer_account(
    current_user: CustomerWithAddressesResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """حذف حساب کاربری"""
    try:
        if not crud.delete_customer(db, current_user["customer"].id):
            raise AuthException(
                status_code=404,
                detail="کاربر یافت نشد",
                error_code="user_not_found"
            )
        return {"message": "حساب کاربری با موفقیت حذف شد"}
    except Exception as e:
        return handle_auth_error(e)

@router.post("/customers/addresses/", response_model=AddressResponse)
async def add_address(
    address_data: AddressCreate,
    current_user: CustomerWithAddressesResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """افزودن آدرس جدید"""
    try:
        address = crud.create_address(
            db,
            current_user["customer"].id,
            address_data
        )
        if not address:
            raise AuthException(
                status_code=404,
                detail="کاربر یافت نشد",
                error_code="user_not_found"
            )
        return address
    except Exception as e:
        return handle_auth_error(e)

@router.get("/customers/addresses/", response_model=list[AddressResponse])
async def get_customer_addresses(
    current_user: CustomerWithAddressesResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت لیست آدرس‌های کاربر"""
    try:
        addresses = crud.get_addresses(db, current_user["customer"].id)
        if not addresses:
            raise AuthException(
                status_code=404,
                detail="آدرسی برای این کاربر یافت نشد",
                error_code="no_addresses"
            )
        return addresses
    except Exception as e:
        return handle_auth_error(e)