from sqlalchemy.orm import Session
from src.auth.model import Customer, Address,OtpStore
from src.auth.schemas import CustomerCreate, CustomerUpdate, AddressCreate
import otp

def generate_and_store_otp(phone: str, db: Session):
    otp = send_otp(phone) 

    if not otp:
        raise HTTPException(status_code=400, detail={"message": "OTP could not be generated or sent."})  

    expires_at = datetime.utcnow() + timedelta(minutes=2) 
    otp_entry = db.query(OtpStore).filter(OtpStore.phone == phone).first()

    if otp_entry:
       if otp_entry.expires_at > datetime.utcnow():
           return otp_entry.otp
       
       otp_entry.otp = otp
       otp_entry.expires_at = expires_at
    else:
       otp_entry = OtpStore(phone=phone, otp=otp, expires_at=expires_at)
       db.add(otp_entry)
    db.commit()
    return otp

def verify_otp(phone: str, otp: int, db: Session):
    otp_entry = db.query(OtpStore).filter(OtpStore.phone == phone, OtpStore.otp == otp).first()
    
    if otp_entry and otp_entry.expires_at > datetime.utcnow():
        return True  
    return False  
def create_customer(db: Session, customer_data: CustomerCreate):
    existing_customer = db.query(Customer).filter(Customer.phone == customer_data.phone).first()
    if existing_customer:
        return None 
    
    new_customer = Customer(**customer_data.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer
def get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer_phone(db: Session, phone: str):
    return db.query(Customer).filter(Customer.phone == phone).first()

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
