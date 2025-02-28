from fastapi import APIRouter, Depends, HTTPException,Header
from sqlalchemy.orm import Session
from database import get_db
from src.auth import crud
from src.auth.schemas import CustomerCreate, CustomerUpdate, CustomerResponse, AddressCreate, AddressResponse,CustomerWithAddressesResponse
from fastapi.security import OAuth2PasswordBearer
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/customers/verify/",auto_error=False)

@router.post("/customers/otp/")
def send_otp(phone: str, db: Session = Depends(get_db)):
    otp = crud.generate_and_store_otp(phone, db)
    return {"message": "OTP sent successfully"}

@router.post("/customers/verify/")
def verify_otp(phone: str, otp: str, db: Session = Depends(get_db)):
    is_valid = crud.verify_otp(phone, otp, db)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    customer,addresses = crud.get_customer_phone(db, phone)

    if customer:
        token_access = crud.access_token(customer.id)
        token_refresh =crud.refresh_token(customer.id,db)
        return {"message": "User already logged in", "data": {"customer": customer,"addresses": addresses},"token_access": token_access,"token_refresh":token_refresh} 
    
    customer_data = CustomerCreate(phone=phone)  
    customer = crud.create_customer(db, customer_data)
    token_access = crud.access_token(customer.id)
    token_refresh =crud.refresh_token(customer.id,db)
    return {"message": "User created successfully", "data": customer, "token_access": token_access,"token_refresh":token_refresh}
@router.post("/customers/refresh/")
def refresh_token(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = crud.verify_token(token)
    if not payload or payload.get("type") != "refresh":
      raise HTTPException(status_code=401, detail={"message": "Invalid Token"})
    ststus=crud.verify_token_refresh(token,db)
    if ststus:
     user_id = payload.get("sub")
     new_access_token = crud.access_token(user_id)
     return {"access_token": new_access_token}
    raise HTTPException(status_code=401, detail={"message": "expired Token"})
@router.post("/customers/logout")
def logout(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = crud.verify_token(token)
    if not payload or payload.get("type") != "refresh":
      raise HTTPException(status_code=401, detail={"message": "Invalid Token"})
    user_id = payload.get("sub")
    status=crud.delete_refresh_token(db,user_id)
    if status:
        return{"logout in successfully"}
    return{"logout in error"}
@router.get("/customers/", response_model=list[CustomerResponse])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip, limit)

@router.get("/customers/found/{phone}", response_model=CustomerWithAddressesResponse)
def read_customer_by_phone( phone: str, db: Session = Depends(get_db)):

    customer, addresses = crud.get_customer_phone(db, phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"customer": customer, "addresses": addresses}
@router.get("/customers/data/", response_model=CustomerWithAddressesResponse)
def read_customer_by_phone(authorization: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    user_id = status.get("sub")
    customer, addresses = crud.get_customer_id(db, user_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer": customer, "addresses": addresses}
@router.put("/customers/edit/", response_model=CustomerResponse)
def update_customer(customer_data: CustomerUpdate, db: Session = Depends(get_db),authorization: str = Depends(oauth2_scheme)):
    if not authorization:
     raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    user_id = status.get("sub")
    customer = crud.update_customer(db, user_id, customer_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer
@router.delete("/customers/deleted/")
def delete_customer( authorization: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    if not authorization:
     raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    user_id = status.get("sub")

    if not crud.delete_customer(db, user_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": "Customer and associated addresses successfully deleted"}

@router.post("/customers/addresses/", response_model=AddressResponse)
def add_address(address_data: AddressCreate, db: Session = Depends(get_db),authorization: str = Depends(oauth2_scheme)):
    if not authorization:
     raise HTTPException(status_code=401, detail="Authorization token is missing")
    status = crud.verify_token(authorization)
    if not status:
        raise HTTPException(status_code=401, detail={"message": "Invalid or expired Token"})
    user_id = status.get("sub")
    address = crud.create_address(db, user_id, address_data)
    if not address:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return address

@router.get("/customers/{customer_id}/addresses/", response_model=list[AddressResponse])
def read_addresses(customer_id: int, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, customer_id)
    if not addresses:
        raise HTTPException(status_code=404, detail="No addresses found for this customer")
    
    return addresses