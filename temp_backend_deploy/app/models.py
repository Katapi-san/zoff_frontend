from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Staff(Base):
    __tablename__ = "staffs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    role = Column(String(50))  # e.g., "Fitting Pro", "Color Master"
    image_url = Column(String(255), nullable=True)
    tags = Column(String(255)) # Comma separated tags for now, or use a separate table
    scope_score = Column(Integer, default=0)
    
    checkins = relationship("CheckIn", back_populates="staff")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    
    checkins = relationship("CheckIn", back_populates="customer")

class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    staff_id = Column(Integer, ForeignKey("staffs.id"), nullable=True) # If they selected a staff
    store_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="checkins")
    staff = relationship("Staff", back_populates="checkins")
