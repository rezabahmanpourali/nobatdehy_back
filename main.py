from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.route import router as auth_router
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from src.barber.routes import router as barber_router
from src.barber_shop.routes import router as barber_shop_router
from src.images.routes import router as image_router
from src.hair_models.routes import router as hair_model_router
from src.category.routes import router as category_router
from src.sms.routes import router as sms_router
target_metadata = Base.metadata 
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)
# PS C:\Users\reza> $env:Path = "C:\Users\reza\AppData\Local\Programs\Python\Python313-arm64;C:\Users\reza\AppData\Local\Programs\Python\Python313-arm64\Scripts;" + $env:Path
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(barber_router, prefix="/barber", tags=["barber"])
app.include_router(barber_shop_router, prefix="/barber_shop", tags=["barber_shop"])
app.include_router(image_router, prefix="/image", tags=["image"])
app.include_router(hair_model_router, prefix="/hair_model", tags=["hair_model"])
app.include_router(sms_router, prefix="/sms", tags=["SMS"])
app.include_router(category_router, prefix="/category", tags=["category"])
# # main.py
# from fastapi import FastAPI
# from database import Base, engine
# from auth.routes import router as auth_router

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Security
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     password = Column(String, nullable=False)

# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
# @app.get('/')
# def init():
#     return {'hello world'}
# # Register endpoint
# @app.post("/register")
# def register(username: str, password: str, db: Session = Depends(get_db)):
#     hashed_password = get_password_hash(password)
#     new_user = User(username=username, password=hashed_password)
#     try:
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return {"message": "User registered successfully"}

# @app.post("/token")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid username or password")
    
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/profile")
# def read_users_me(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     return {"message": "Welcome to your profile"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)