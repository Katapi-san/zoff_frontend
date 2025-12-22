from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

class TagBase(BaseModel):
    name: str
    type: Optional[str] = None
    certification_source: Optional[str] = None
    icon_url: Optional[str] = None

class Tag(TagBase):
    id: int
    class Config:
        from_attributes = True

class StoreSummary(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class StaffBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    role: Optional[str] = None
    image_url: Optional[str] = None
    scope_score: Optional[int] = 0
    introduction: Optional[str] = None

class StaffCreate(StaffBase):
    store_id: Optional[int] = None

class Staff(StaffBase):
    id: int
    store_id: Optional[int] = None
    store: Optional[StoreSummary] = None
    tags: List[Tag] = []
    class Config:
        from_attributes = True

class StoreBase(BaseModel):
    name: str
    prefecture: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    congestion_url: Optional[str] = None
    opening_hours: Optional[str] = None
    phone_number: Optional[str] = None
    remarks: Optional[str] = None

class Store(StoreBase):
    id: int
    # staff: List[Staff] = [] # Avoid circular dependency or large payload unless needed
    class Config:
        from_attributes = True

class PurchaseHistory(BaseModel):
    id: int
    purchase_date: Optional[date]
    frame_model: Optional[str]
    lens_r: Optional[str]
    lens_l: Optional[str]
    warranty_info: Optional[str]
    prescription_pd: Optional[float]
    prescription_r_sph: Optional[float]
    prescription_r_cyl: Optional[float]
    prescription_r_axis: Optional[int]
    prescription_l_sph: Optional[float]
    prescription_l_cyl: Optional[float]
    prescription_l_axis: Optional[int]
    class Config:
        from_attributes = True

class CustomerPreferredTag(BaseModel):
    tag: Tag
    class Config:
        from_attributes = True

class Customer(BaseModel):
    id: int
    name: Optional[str]
    kana: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    profile: Optional[str]
    image_url: Optional[str]
    
    purchase_histories: List[PurchaseHistory] = []
    preferred_tags: List[CustomerPreferredTag] = []
    
    class Config:
        from_attributes = True

class Reservation(BaseModel):
    id: int
    store_id: int
    customer_id: int
    staff_id: Optional[int]
    reservation_time: datetime
    status: str
    memo: Optional[str]
    
    customer: Optional[Customer]
    staff: Optional[Staff]
    
    class Config:
        from_attributes = True
