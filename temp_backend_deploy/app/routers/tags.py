from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.store import Tag, Staff, StaffTag
from app import schemas

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)

@router.get("/", response_model=List[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags

@router.get("/{tag_id}/staff", response_model=List[schemas.Staff])
def read_staff_by_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Return staff associated with this tag
    return tag.staff
