from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db
from app.models.store import Store, Staff

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.Store])
def read_stores(
    prefecture: Optional[str] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    query = db.query(Store)
    if prefecture:
        query = query.filter(Store.prefecture == prefecture)
    if city:
        query = query.filter(Store.city == city)
    stores = query.offset(skip).limit(limit).all()
    return stores

@router.get("/{store_id}", response_model=schemas.Store)
def read_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

@router.get("/{store_id}/staff", response_model=List[schemas.Staff])
def read_store_staff(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    
    # Deduplicate staff by display_name
    unique_staff = []
    seen_names = set()
    for s in store.staff:
        # Use display_name if available, otherwise name
        name_key = s.display_name if s.display_name else s.name
        if name_key not in seen_names:
            unique_staff.append(s)
            seen_names.add(name_key)
            
    return unique_staff
