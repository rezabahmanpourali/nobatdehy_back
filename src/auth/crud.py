from sqlalchemy.orm import Session
from src.auth.model import Customer, Address
from src.auth.schemas import CustomerCreate, CustomerUpdate, AddressCreate

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
