import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from src.barber.routes import router as barber_router
from src.barber_shop.routes import router as barber_shop_router
from src.images.routes import router as image_router
from src.hair_models.routes import router as hair_model_router
from src.category.routes import router as category_router
from src.working_hours.routes import router as working_hours_router

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

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

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

Base.metadata.create_all(bind=engine)

app.include_router(barber_router, prefix="/barber", tags=["barber"])
app.include_router(barber_shop_router, prefix="/barber_shop", tags=["barber_shop"])
app.include_router(image_router, prefix="/image", tags=["image"])
app.include_router(hair_model_router, prefix="/hair_model", tags=["hair_model"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(working_hours_router, prefix="/working_hours", tags=["working_hours"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
