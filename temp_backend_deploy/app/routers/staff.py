from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.models import Staff

router = APIRouter(
    prefix="/staffs",
    tags=["staffs"],
)

@router.post("/", response_model=schemas.Staff)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    db_staff = Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.get("/", response_model=List[schemas.Staff])
def read_staffs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    staffs = db.query(Staff).offset(skip).limit(limit).all()
    return staffs

@router.get("/{staff_id}", response_model=schemas.Staff)
def read_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff
