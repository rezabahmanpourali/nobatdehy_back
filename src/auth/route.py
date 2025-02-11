from fastapi import APIRouter, Depends, HTTPException,Header
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
    customer_data = CustomerCreate(phone=phone)  
    customer,addresses = crud.get_customer_phone(db, phone)

    if customer:
        token = crud.create_access_token(customer.id)
        return {"message": "User already logged in", "data": {"customer": customer,"addresses": addresses},"token": token} 
    
    customer = crud.create_customer(db, customer_data)
    token = crud.create_access_token(customer.id)
    return {"message": "User created successfully", "data": customer, "token": token}
@router.post("/customers/refresh/")
def refresh_token(token:str):
    exp_tok=crud.refresh_token(token)
    token = crud.create_access_token(exp_tok)
    return {"token": token}
@router.get("/customers/", response_model=list[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip, limit)

@router.get("/customers/found/{phone}", response_model=CustomerWithAddressesResponse)
def read_customer_by_phone( phone: str, db: Session = Depends(get_db)):

    customer, addresses = crud.get_customer_phone(db, phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"customer": customer, "addresses": addresses}
@router.get("/customers/data/{authorization}", response_model=CustomerWithAddressesResponse)
def read_customer_by_phone(authorization: str, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_access_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    customer, addresses = crud.get_customer_id(db, status)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer": customer, "addresses": addresses}
@router.put("/customers/edit/", response_model=CustomerResponse)
def update_customer(customer_data: CustomerUpdate, db: Session = Depends(get_db),authorization: str = Header(None)):
    if not authorization:
     raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_access_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    
    customer = crud.update_customer(db, status, customer_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer
@router.delete("/customers/deleted/{authorization}")
def delete_customer( authorization: str,db: Session = Depends(get_db)):
    if not authorization:
     raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_access_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    if not crud.delete_customer(db, status):
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": "Customer and associated addresses successfully deleted"}

@router.post("/customers/addresses/", response_model=AddressResponse)
def add_address(address_data: AddressCreate, db: Session = Depends(get_db),authorization: str = Header(None)):
    if not authorization:
     raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_access_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    
    address = crud.create_address(db, status, address_data)
    if not address:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return address

@router.get("/customers/{customer_id}/addresses/", response_model=list[AddressResponse])
def read_addresses(customer_id: int, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, customer_id)
    if not addresses:
        raise HTTPException(status_code=404, detail="No addresses found for this customer")
    
    return addresses