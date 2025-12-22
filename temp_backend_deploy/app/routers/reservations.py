from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)

@router.get("/", response_model=List[schemas.Reservation])
def read_reservations(
    store_id: int = Query(..., description="Store ID to filter reservations"),
    date_str: Optional[str] = Query(None, alias="date", description="Date in YYYY-MM-DD format"),
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Reservation).filter(models.Reservation.store_id == store_id)
    
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # SQLite doesn't have DATE type strictly, but SQLAlchemy handles it if mapped correctly.
            # Or filtering by range of the day.
            # Assuming 'reservation_time' is DateTime.
            query = query.filter(models.Reservation.reservation_time >= datetime.combine(target_date, datetime.min.time()))
            query = query.filter(models.Reservation.reservation_time <= datetime.combine(target_date, datetime.max.time()))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")

    if start_date and end_date:
        try:
            s_date = datetime.strptime(start_date, '%Y-%m-%d')
            e_date = datetime.strptime(end_date, '%Y-%m-%d')
             # End date extended to end of day
            e_date_end = datetime.combine(e_date.date(), datetime.max.time())
            
            query = query.filter(models.Reservation.reservation_time >= s_date)
            query = query.filter(models.Reservation.reservation_time <= e_date_end)
        except ValueError:
             raise HTTPException(status_code=400, detail="Invalid date range format")

    reservations = query.all()
    return reservations

@router.get("/{reservation_id}", response_model=schemas.Reservation)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

# Also expose a helper to get reservations via store route?
# No, easier to keep it here with query param.
