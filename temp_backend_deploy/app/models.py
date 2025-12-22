from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    prefecture = Column(String, index=True)
    city = Column(String, index=True, nullable=True)
    address = Column(String, nullable=True)
    congestion_url = Column(String, nullable=True)
    opening_hours = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    
    staff = relationship("Staff", back_populates="store")


class Staff(Base):
    __tablename__ = "staff" # Singular in DB

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    display_name = Column(String)
    role = Column(String) 
    image_url = Column(String, nullable=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    
    store = relationship("Store")
    tags = relationship("Tag", secondary="staff_tags", back_populates="staff")

class StaffTag(Base):
    __tablename__ = "staff_tags"
    
    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    endorsement_count = Column(Integer, default=0)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    kana = Column(String)
    gender = Column(String)
    age = Column(Integer)
    profile = Column(String)
    image_url = Column(String)
    
    purchase_histories = relationship("PurchaseHistory", back_populates="customer")
    reservations = relationship("Reservation", back_populates="customer")
    preferred_tags = relationship("CustomerPreferredTag", back_populates="customer")

class PurchaseHistory(Base):
    __tablename__ = "purchase_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    purchase_date = Column(Date)
    frame_model = Column(String)
    lens_r = Column(String)
    lens_l = Column(String)
    warranty_info = Column(String)
    # Prescription
    prescription_pd = Column(Float)
    prescription_r_sph = Column(Float)
    prescription_r_cyl = Column(Float)
    prescription_r_axis = Column(Integer)
    prescription_l_sph = Column(Float)
    prescription_l_cyl = Column(Float)
    prescription_l_axis = Column(Integer)
    
    customer = relationship("Customer", back_populates="purchase_histories")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    staff = relationship("Staff", secondary="staff_tags", back_populates="tags")


class CustomerPreferredTag(Base):
    __tablename__ = "customer_preferred_tags"
    customer_id = Column(Integer, ForeignKey("customers.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    
    customer = relationship("Customer", back_populates="preferred_tags")
    tag = relationship("Tag")

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    staff_id = Column(Integer, ForeignKey("staff.id"))
    reservation_time = Column(DateTime)
    status = Column(String)
    memo = Column(Text)
    
    store = relationship("Store")
    customer = relationship("Customer", back_populates="reservations")
    staff = relationship("Staff")

