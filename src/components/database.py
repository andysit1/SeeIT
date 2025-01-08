from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List

Base = declarative_base()

# For now ill just keep all my models here for now
# any time we need a specific function we write it here to pull and add -> its more flexible and fast for me now.

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



# SQLAlchemy Database Setup
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def add_more_media_to_bin(bin_id, new_media_items):
    """
    Add more media objects to an existing bin.

    :param bin_id: The ID of the bin to update.
    :param new_media_items: A list of MediaCreate objects to add.
    """
    session = SessionLocal()
    try:
        # Fetch the existing bin
        db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
        if not db_bin:
            print(f"Bin with bin_id {bin_id} not found.")
            return

        # Create Media objects and append them
        for media_data in new_media_items:
            new_media = Media(
                date=media_data.date,
                type=media_data.type,
                content=media_data.content
            )
            db_bin.media_items.append(new_media)

        # Commit changes
        session.commit()
        print(f"Added {len(new_media_items)} media items to Bin {bin_id}.")
    except Exception as e:
        session.rollback()
        print(f"Error adding media to bin: {e}")
    finally:
        session.close()



def create_new_bin(description : str, b_id: int, link: str):
    session = SessionLocal()

    try:
        # Create a Bin object with no media content
        new_bin = Bin(
            description=description,
            bin_id=b_id,
            link=link,
            media_items=[

            ]
        )
        session.add(new_bin)
        session.commit()
    except:
        print("Bin ID already exists.")


# Test Script
def test_bin_and_media():
    # Create a new session
    session = SessionLocal()

    try:
        # Create a Bin object with associated Media
        new_bin = Bin(
            description="Test Bin",
            bin_id=1,
            link="http://example.com",
            media_items=[
                Media(date=datetime.now(), type="text", content="Sample text content"),
                Media(date=datetime.now(), type="image", content="image.png")
            ]
        )

        session.add(new_bin)
        session.commit()

        # Fetch the Bin from the database
        db_bin = session.query(Bin).filter(Bin.bin_id == 1).first()

        # Convert to Pydantic model
        bin_response = BinResponse.model_validate(obj=db_bin, from_attributes=True)

        # Print the Pydantic response
        print(bin_response.model_dump_json(indent=4))

        # Close session
        session.close()
    except:
        print("Bin ID already exists.")


#pretty much a DB practice function
def fetch_bin_with_media(bin_id):
    session = SessionLocal()
    try:
        db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
        if db_bin:
            bin_response = BinResponse.model_validate(obj=db_bin, from_attributes=True)
            print(bin_response.model_dump_json(indent=4))
        else:
            print(f"Bin with bin_id {bin_id} not found.")
    finally:
        session.close()


def remove_all_media_from_bin(bin_id: int):
    session = SessionLocal()

    try:
        # Fetch the Bin object
        db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
        if db_bin:
            # Remove all associated media
            for media in db_bin.media_items:
                session.delete(media)
            session.commit()
            print(f"All media items associated with Bin ID {bin_id} have been deleted.")
        else:
            print(f"No Bin found with Bin ID {bin_id}.")
    finally:
        session.close()


def remove_bin(bin_id: int):
    session = SessionLocal()

    try:
        # Fetch the Bin object
        db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
        if db_bin:
            session.delete(db_bin)  # This will also delete associated Media items
            session.commit()
            print(f"Bin with ID {bin_id} and its media items have been deleted.")
        else:
            print(f"No Bin found with Bin ID {bin_id}.")
    finally:
        session.close()
