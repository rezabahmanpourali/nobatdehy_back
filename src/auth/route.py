from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.auth import crud
from src.auth.schemas import CustomerCreate, CustomerUpdate, CustomerResponse, AddressCreate, AddressResponse,CustomerWithAddressesResponse

router = APIRouter()
@router.post("/customers/otp/")
def send_otp(phone: str, db: Session = Depends(get_db)):
    otp = crud.generate_and_store_otp(phone, db)
    return {"message": "OTP sent successfully"}

@router.post("/customers/verify/")
def verify_otp(phone: str, otp: str, db: Session = Depends(get_db)):
    is_valid = crud.verify_otp(phone, otp, db)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    token = crud.create_access_token(phone)
    customer_data = CustomerCreate(phone=phone)  # این قسمت را اضافه کن
    customer = crud.get_customer_phone(db, phone)
    if customer:
        return {"message": "User already logged in", "data": customer, "token": token}  # کاربر از قبل لاگین شده است
    
    customer = crud.create_customer(db, customer_data)
    return {"message": "User created successfully", "data": customer, "token": token}

@router.get("/customers/", response_model=list[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip, limit)

@router.get("/customers/login/{token}/{phone}", response_model=CustomerWithAddressesResponse)
def read_customer_by_phone(a_token: str, phone: str, db: Session = Depends(get_db)):
    status = crud.verify_access_token(a_token)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    
    customer, addresses = crud.get_customer_phone(db, phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"customer": customer, "addresses": addresses}

@router.put("/customers/edit/{token}/{customer_id}/", response_model=CustomerResponse)
def update_customer(a_token: str, customer_id: int, customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    status = crud.verify_access_token(a_token)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    
    customer = crud.update_customer(db, customer_id, customer_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer

@router.delete("/customers/deleted/{token}/{customer_id}/")
def delete_customer(a_token: str, customer_id: int, db: Session = Depends(get_db)):
    status = crud.verify_access_token(a_token)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    
    if not crud.delete_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": "Customer and associated addresses successfully deleted"}

@router.post("/customers/{token}/{customer_id}/addresses/", response_model=AddressResponse)
def add_address(a_token: str, customer_id: int, address_data: AddressCreate, db: Session = Depends(get_db)):
    status = crud.verify_access_token(a_token)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    
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