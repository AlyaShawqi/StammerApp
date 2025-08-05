# routes/kids.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, validator
from db.models import Kid, User, AgeGroupEnum, GenderEnum
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime
from routes.auth import verify_token
from utils.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/kids", tags=["Kids"])

class KidSignupData(BaseModel):
    name: str
    age_group: AgeGroupEnum
    gender: GenderEnum

    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Kid name must be at least 2 characters long')
        if len(v.strip()) > 50:
            raise ValueError('Kid name must be less than 50 characters')
        return v.strip()

class KidResponse(BaseModel):
    id: int
    name: str
    age_group: AgeGroupEnum
    gender: GenderEnum
    created_at: datetime
    parent_id: int

    class Config:
        from_attributes = True

@router.post("/signup", response_model=KidResponse, status_code=status.HTTP_201_CREATED)
def signup_kid(
    data: KidSignupData,
    parent_email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    try:
        parent = db.query(User).filter(User.email == parent_email).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent user not found")

        existing_kid = db.query(Kid).filter(Kid.parent_id == parent.id, Kid.name == data.name).first()
        if existing_kid:
            raise HTTPException(status_code=400, detail=f"Kid '{data.name}' already exists")

        new_kid = Kid(
            parent_id=parent.id,
            name=data.name,
            age_group=data.age_group,
            gender=data.gender
        )
        db.add(new_kid)
        db.commit()
        db.refresh(new_kid)

        return new_kid

    except Exception as e:
        db.rollback()
        logger.error(f"Kid signup error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[KidResponse])
def get_kids(
    parent_email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    try:
        parent = db.query(User).filter(User.email == parent_email).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")

        kids = db.query(Kid).filter(Kid.parent_id == parent.id).all()
        return kids

    except Exception as e:
        logger.error(f"Get kids error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
