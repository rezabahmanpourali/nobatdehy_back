from sqlalchemy.orm import Session
from src.auth.model import Customer, Address,OtpStore
from src.auth.schemas import CustomerCreate, CustomerUpdate, AddressCreate,AddressResponse,CustomerOtp,CustomerResponse,CustomerUpdate
from src.auth import otp
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException
import jwt
from fastapi import HTTPException

SECRET_KEY = "barber"
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE_MINUTES = 10  # مدت زمان اعتبار توکن

# ایجاد توکن برای کاربر
def create_access_token(id: int):
    ids=str(id)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": ids, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def refresh_token(token:str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = (payload["sub"]) 
    return user_id
# اعتبارسنجی توکن
def verify_access_token(token: str, customer_id: int):
        # دیکود کردن توکن
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        exp_time = datetime.utcfromtimestamp(payload["exp"]).replace(tzinfo=timezone.utc)
        user_id = (payload["sub"]) 

        if exp_time < datetime.now(timezone.utc) or str(user_id) != str(customer_id):
            return False  
        
        return True 
    
def generate_and_store_otp(phone: str, db: Session):
    generated_otp = otp.send_otp(phone)  

    if not generated_otp:
        raise HTTPException(status_code=400, detail={"message": "OTP could not be generated or sent."})  

    expires_at = datetime.utcnow() + timedelta(minutes=180) 
    otp_entry = db.query(OtpStore).filter(OtpStore.phone == phone).first()

    if otp_entry:
       if otp_entry.expires_at > datetime.utcnow():
           return otp_entry.otp
       
       otp_entry.otp = generated_otp
       otp_entry.expires_at = expires_at
    else:
       otp_entry = OtpStore(phone=phone, otp=generated_otp, expires_at=expires_at)
       db.add(otp_entry)
    db.commit()
    return generated_otp  # استفاده از نام جدید


def verify_otp(phone: str, otp: int, db: Session):
    otp_entry = db.query(OtpStore).filter(OtpStore.phone == phone, OtpStore.otp == otp).first()
    
    if otp_entry and otp_entry.expires_at > datetime.utcnow():
        return True  # OTP صحیح است
    return False  # OTP نامعتبر یا منقضی شده
def create_customer(db: Session, customer_data: CustomerCreate):
    existing_customer = db.query(Customer).filter(Customer.phone == customer_data.phone).first()
    if existing_customer:
        return None 
        #یادآوری تغییر
    if not customer_data.name:
        customer_data.name = "1"
    if not customer_data.lastn:
        customer_data.lastn = "2"
    new_customer = Customer(**customer_data.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer
def get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer_phone(db: Session, phone: str):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        addresses = db.query(Address).filter(Address.customer_id == customer.id).all()
        return customer, addresses
    return None, None
def get_customer_id(db: Session, id: str):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if customer:
        addresses = db.query(Address).filter(Address.customer_id == id).all()
        return customer, addresses
    return None, None


def update_customer(db: Session, customer_id: int, customer_data: CustomerUpdate):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    for key, value in customer_data.dict().items():
        setattr(customer, key, value)

    db.commit()
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return False

    db.query(Address).filter(Address.customer_id == customer_id).delete()

    db.delete(customer)
    db.commit()
    return True
def create_address(db: Session, customer_id: int, address_data: AddressCreate):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    new_address = Address(customer_id=customer_id, **address_data.dict())
    db.add(new_address)
    db.commit()
    return new_address

def get_addresses(db: Session, customer_id: int):
    return db.query(Address).filter(Address.customer_id == customer_id).all()
