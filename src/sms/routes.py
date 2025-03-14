from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

from database import get_db
from .models import SMS

router = APIRouter()

@router.post("/")
async def create_sms(sms_data: dict, db: Session = Depends(get_db)):
    try:
        # Handle both single SMS and list of SMS
        if isinstance(sms_data, list):
            sms_list = []
            for msg in sms_data:
                new_sms = SMS(
                    sender=msg['sender'],
                    body=msg['body'],
                    timestamp=datetime.fromisoformat(msg['timestamp'])
                )
                db.add(new_sms)
                sms_list.append(new_sms)
            db.commit()
            for sms in sms_list:
                db.refresh(sms)
            return {"message": f"Successfully created {len(sms_list)} SMS records"}
        else:
            new_sms = SMS(
                sender=sms_data['sender'],
                body=sms_data['body'],
                timestamp=datetime.fromisoformat(sms_data['timestamp'])
            )
            db.add(new_sms)
            db.commit()
            db.refresh(new_sms)
            return {"message": "SMS created successfully", "id": new_sms.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
def get_sms_list(db: Session = Depends(get_db)):
    sms_list = db.query(SMS).all()
    return [
        {
            "id": sms.id,
            "sender": sms.sender,
            "body": sms.body,
            "timestamp": sms.timestamp.isoformat()
        }
        for sms in sms_list
    ]

@router.get("/{sms_id}", response_model=dict)
def get_sms(sms_id: int, db: Session = Depends(get_db)):
    sms = db.query(SMS).filter(SMS.id == sms_id).first()
    if not sms:
        raise HTTPException(status_code=404, detail="SMS not found")
    return {
        "id": sms.id,
        "sender": sms.sender,
        "body": sms.body,
        "timestamp": sms.timestamp.isoformat()
    }

@router.delete("/{sms_id}")
def delete_sms(sms_id: int, db: Session = Depends(get_db)):
    sms = db.query(SMS).filter(SMS.id == sms_id).first()
    if not sms:
        raise HTTPException(status_code=404, detail="SMS not found")
    db.delete(sms)
    db.commit()
    return {"message": "SMS deleted successfully"} 