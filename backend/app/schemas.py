from pydantic import BaseModel
from typing import List, Optional

class StaffBase(BaseModel):
    name: str
    role: str
    image_url: Optional[str] = None
    tags: Optional[str] = None
    scope_score: int = 0

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id: int

    class Config:
        orm_mode = True

class CheckInBase(BaseModel):
    store_id: int
    staff_id: Optional[int] = None

class CheckInCreate(CheckInBase):
    customer_id: int

class CheckIn(CheckInBase):
    id: int
    timestamp: str

    class Config:
        orm_mode = True
