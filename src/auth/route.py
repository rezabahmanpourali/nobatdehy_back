from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.auth import crud
from src.auth.schemas import CustomerCreate, CustomerUpdate, CustomerResponse, AddressCreate, AddressResponse

router = APIRouter()
@router.post("/customers/otp/")
def send_otp(phone: str, db: Session = Depends(get_db)):
    otp = crud.generate_and_store_otp(phone, db)
    return {"message": "OTP sent successfully"}

@router.post("/customers/verify/")
def verify_otp(phone: str, otp: int, db: Session = Depends(get_db)):
    is_valid = crud.verify_otp(phone, otp, db)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    customer = crud.get_customer_phone(db, phone)
    if not customer:
        customer = crud.create_customer(db, {"phone": phone})

    return {"message": "OTP verified successfully", "customer": customer}
@router.get("/customers/", response_model=list[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip, limit)

@router.get("/customers/login/{phone}", response_model=CustomerResponse)
def read_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    customer = crud.get_customer_phone(db, phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/customers/edit/{customer_id}/", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    customer = crud.update_customer(db, customer_id, customer_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/customers/deleted/{customer_id}/")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    if not crud.delete_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer and associated addresses successfully deleted"}

@router.post("/customers/{customer_id}/addresses/", response_model=AddressResponse)
def add_address(customer_id: int, address_data: AddressCreate, db: Session = Depends(get_db)):
    address = crud.create_address(db, customer_id, address_data)
    if not address:
        raise HTTPException(status_code=404, detail="Customer not found")
    return address

@router.get("/customers/{customer_id}/addresses/", response_model=list[AddressResponse])
def read_addresses(customer_id: int, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, customer_id)
    if not addresses:
        raise HTTPException(status_code=404, detail="No addresses found for this customer")
    return addresses

