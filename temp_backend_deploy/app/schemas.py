from pydantic import BaseModel
from typing import List, Optional

class TagBase(BaseModel):
    name: str
    type: str
    certification_source: Optional[str] = None
    icon_url: Optional[str] = None

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

class StaffBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    role: Optional[str] = None
    image_url: Optional[str] = None
    scope_score: int = 0
    privacy_level: str = "PUBLIC"
    status: str = "WORKING"
    introduction: Optional[str] = None

class StaffCreate(StaffBase):
    pass

class StoreSummary(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Staff(StaffBase):
    id: int
    store_id: Optional[int] = None
    store: Optional[StoreSummary] = None
    tags: List[Tag] = []

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

class StoreBase(BaseModel):
    name: str
    prefecture: str
    city: str
    address: Optional[str] = None
    congestion_url: Optional[str] = None
    opening_hours: Optional[str] = None
    phone_number: Optional[str] = None
    remarks: Optional[str] = None

class Store(StoreBase):
    id: int
    staff: List[Staff] = []

    class Config:
        orm_mode = True
