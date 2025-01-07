from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Text, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
from sqlalchemy import create_engine

from pydantic import BaseModel, Field
from typing import List, Optional


Base = declarative_base()


#sqlacademy objects
class Bin(Base):
    __tablename__ = 'bins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    bin_id = Column(Integer, unique=True, nullable=False)
    link = Column(String, nullable=False)

    # One-to-many relationship with Media
    media_items = relationship("Media", back_populates="bin")

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bin_id = Column(Integer, ForeignKey('bins.id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    type = Column(String, nullable=False)  # Classification of media type (e.g., text, image)
    content = Column(Text, nullable=False)  # Text or path to image content

    # Relationship back to Bin
    bin = relationship("Bin", back_populates="media_items")

#pydantic objects might
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
        orm_mode = True

class BinBase(BaseModel):
    description: str
    bin_id: int
    link: str

class BinCreate(BinBase):
    media_items: List[MediaCreate] = Field(default_factory=list)

class BinResponse(BinBase):
    id: int #the primary key in the db...
    media_items: List[MediaResponse] = Field(default_factory=list)

    class Config:
        orm_mode = True

