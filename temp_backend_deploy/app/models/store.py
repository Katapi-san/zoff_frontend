from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    prefecture = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String, nullable=True)
    congestion_url = Column(String, nullable=True)
    opening_hours = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    remarks = Column(String, nullable=True)

    staff = relationship("Staff", back_populates="store")

class StaffTag(Base):
    __tablename__ = "staff_tags"

    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    endorsement_count = Column(Integer, default=0)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String) # EXPERT, OFFICIAL, CASUAL
    certification_source = Column(String, nullable=True) # LMS, SELF
    icon_url = Column(String, nullable=True)

    staff = relationship("Staff", secondary="staff_tags", back_populates="tags")

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    # Basic Info
    name = Column(String, index=True) # Keeping for backward compatibility or internal name
    display_name = Column(String, index=True) # Zoff Name
    real_name = Column(String, nullable=True)
    role = Column(String, nullable=True)
    
    # Store Relation
    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("Store", back_populates="staff")

    # Privacy & Display
    privacy_level = Column(String, default="PUBLIC") # PUBLIC, PRIME_ONLY, SECRET
    display_options = Column(String, nullable=True) # JSON string
    avatar_config = Column(String, nullable=True)
    status = Column(String, default="WORKING") # WORKING, BREAK, OFF
    image_url = Column(String, nullable=True)
    scope_score = Column(Integer, default=0)
    introduction = Column(String, nullable=True)

    # Tags
    tags = relationship("Tag", secondary="staff_tags", back_populates="staff")
