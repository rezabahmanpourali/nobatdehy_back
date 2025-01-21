from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from src.images.schemas import ImageCreate, ImageResponse
from src.images.crud import create_image, get_images_by_entity
from src.images.utils import s3_client, BUCKET_NAME

router = APIRouter()

@router.post("/upload/", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    barber_shop_id: int = None,
    barber_id: int = None,
    hair_model_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db),
):
    try:
        file_name = f"uploads/{file.filename}"

        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file_name,
            ExtraArgs={"ContentType": file.content_type},
        )

        file_url = f"https://{BUCKET_NAME}.storage.c2.liara.space/{file_name}"

        image_data = ImageCreate(
            file_name=file.filename,
            url=file_url,
            barber_shop_id=barber_shop_id,
            barber_id=barber_id,
            hair_model_id=hair_model_id,
            category_id=category_id
        )
        new_image = create_image(db, image_data)

        return ImageResponse.from_orm(new_image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/images/", response_model=list[ImageResponse])
def get_images(
    barber_shop_id: int = None,
    barber_id: int = None,
    hair_model_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db),
    
):
    images = get_images_by_entity(db, barber_shop_id, barber_id, hair_model_id,category_id) 
    return images