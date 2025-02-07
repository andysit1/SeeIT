# hold user, bin, media.


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List

Base = declarative_base()

from src2.util import generate_bin_id

# For now ill just keep all my models here for now
# any time we need a specific function we write it here to pull and add -> its more flexible and fast for me now.

#Issues
    # how do i make the user be created without the other bin, media

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)  # Example of additional user info
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with Bin
    bins = relationship("Bin", back_populates="user")

# Bin Model
class Bin(Base):
    __tablename__ = 'bins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    bin_id = Column(Integer, unique=True, nullable=False)
    link = Column(String, nullable=False)

    # Foreign Key and Relationship with User
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="bins")

    # One-to-many relationship with Media
    media_items = relationship("Media", back_populates="bin")

# Media Model
class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bin_id = Column(Integer, ForeignKey('bins.id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    type = Column(Integer, nullable=False)  # Classification of media type (e.g., text, image)
    content = Column(Text, nullable=False)  # Text or path to image content
    # Relationship back to Bin
    bin = relationship("Bin", back_populates="media_items")

# Media Pydantic Models
class MediaBase(BaseModel):
    date: datetime
    type: str
    content: str

class MediaCreate(MediaBase):
    pass

class MediaResponse(MediaBase):
    id: int
    bin_id: int

    class Config:
        from_attributes = True

# Bin Pydantic Models
class BinBase(BaseModel):
    description: str
    bin_id : str = generate_bin_id()

class BinCreate(BinBase):
    media_items: List[MediaCreate] = Field(default_factory=list)
    user_id: int

class BinResponse(BinBase):
    id: int
    media_items: List[MediaResponse] = Field(default_factory=list)
    user_id: int

    class Config:
        from_attributes = True

# User Pydantic Models
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    bins: List[BinResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True





