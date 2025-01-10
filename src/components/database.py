from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List

Base = declarative_base()

# For now ill just keep all my models here for now
# any time we need a specific function we write it here to pull and add -> its more flexible and fast for me now.

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
    type = Column(String, nullable=False)  # Classification of media type (e.g., text, image)
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
    bin_id: int
    link: str

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


# SQLAlchemy Database Setup
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def is_user_exist_by_username(username: str) -> bool:
    """
    Check if a user with the given username already exists in the database.

    :param email: The username to check.
    :return: True if the user exists, False otherwise.
    """
    session = SessionLocal()
    try:
        # Query the database for a user with the given email
        user = session.query(User).filter(User.username == username).first()
        return user is not None
    finally:
        session.close()

def is_user_exist_by_email(email: str) -> bool:
    """
    Check if a user with the given email already exists in the database.

    :param email: The email to check.
    :return: True if the user exists, False otherwise.
    """
    session = SessionLocal()
    try:
        # Query the database for a user with the given email
        user = session.query(User).filter(User.email == email).first()
        return user is not None
    finally:
        session.close()


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



def fetch_user_by_email(email):
    session = SessionLocal()
    try:
        db_bin = session.query(User).filter(User.email == email).first()
        if db_bin:
            user_response = UserResponse.model_validate(obj=db_bin, from_attributes=True)
            print(user_response.model_dump_json(indent=4))
        else:
            print(f"User with user_id {email} not found.")
    finally:
        session.close()

#pretty much a DB practice function
def fetch_bin_with_media(bin_id):
    session = SessionLocal()
    try:
        db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
        if db_bin:
            bin_response = BinResponse.model_validate(obj=db_bin, from_attributes=True)
            print(bin_response.model_dump_json(indent=4))
            return bin_response
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


# Functions
def get_bins_by_userid(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user_response = UserResponse.model_validate(obj=user, from_attributes=True)
            print(user_response.model_dump_json(indent=4))
        else:
            print(f"User with ID {user_id} not found.")
    finally:
        session.close()


def get_user(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user_response = UserResponse.model_validate(obj=user, from_attributes=True)
            print(user_response.model_dump_json(indent=4))
            return user_response
        else:
            print(f"User with ID {user_id} not found.")
    finally:
        session.close()

def create_user(username:str, password:str, email:str) -> UserResponse:
    session = SessionLocal()
    try:
        if not is_user_exist_by_email(email) and not is_user_exist_by_username(username):
            new_user = User(username=username, password=password, email=email)
            session.add(new_user)
            session.commit()

            user_response = UserResponse.model_validate(new_user)
            return user_response
        else:
            print(f"User already exists")
    except:
        print(f'Unable to create user')
    finally:
        session.close()

def create_bin(bin_create_obj: BinCreate) -> BinResponse:
    session = SessionLocal()
    try:
        user_response = get_user(bin_create_obj.user_id)

        if user_response:
            new_bin = Bin(
                description=bin_create_obj.description,
                bin_id = bin_create_obj.bin_id,
                link=bin_create_obj.link,
                user_id=bin_create_obj.user_id
            )
            session.add(new_bin)
            session.commit()
            return BinResponse.model_validate(new_bin)
        else:
            print("Given user_id does not exist")
    except Exception as e:
        print(f"Unable to create bin: {e}")
    finally:
        session.close()

# Example Usage
def example():
    session = SessionLocal()
    try:
        # Create a user
        new_user = User(username="test_user", password="securepass", email="test@example.com")
        session.add(new_user)
        session.commit()

        # Create a bin associated with the user
        new_bin = Bin(description="User's Bin", bin_id=100, link="http://example.com", user_id=new_user.id)
        session.add(new_bin)
        session.commit()

        # Fetch and display the user's bins
        get_bins_by_userid(new_user.id)

        # Add media to the bin
        add_more_media_to_bin(100, [
            MediaCreate(date=datetime.now(), type="text", content="Example content"),
            MediaCreate(date=datetime.now(), type="image", content="image.png")
        ])

        # Fetch and display the bin
        fetch_bin_with_media(100)
        try:
            fetch_user_by_email("test@example.com")
        except:
            print("fetch_user_by_email() not working")

        try:
            get_user(1)
        except:
            print("fetch_user_by_email() not working")


    finally:
        session.close()


#Test Cases -> basic test cases ai generated just to see what i should be doing... future will implement test dir with pytest

def test_create_new_bin():
    # Arrange
    bin_data = {
        'description': "Test Bin 2",
        'b_id': 2,
        'link': "http://example2.com"
    }

    # Act
    create_new_bin(bin_data['description'], bin_data['b_id'], bin_data['link'])

    # Assert
    session = SessionLocal()
    db_bin = session.query(Bin).filter(Bin.bin_id == bin_data['b_id']).first()
    assert db_bin is not None
    assert db_bin.description == bin_data['description']
    assert db_bin.link == bin_data['link']
    session.close()

def test_add_more_media_to_bin():
    # Arrange
    bin_id = 1
    media_items = [
        MediaCreate(date=datetime.now(), type="text", content="New media content")
    ]

    # Act
    add_more_media_to_bin(bin_id, media_items)

    # Assert
    session = SessionLocal()
    db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
    assert db_bin is not None
    assert len(db_bin.media_items) == 3  # Assuming there were already 2 media items
    session.close()



def test_remove_all_media_from_bin():
    # Arrange
    bin_id = 1

    # Act
    remove_all_media_from_bin(bin_id)

    # Assert
    session = SessionLocal()
    db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
    assert len(db_bin.media_items) == 0
    session.close()


def test_remove_bin():
    # Arrange
    bin_id = 2

    # Act
    remove_bin(bin_id)

    # Assert
    session = SessionLocal()
    db_bin = session.query(Bin).filter(Bin.bin_id == bin_id).first()
    assert db_bin is None
    session.close()


if __name__ == "__main__":
    #for now just use example to test usecase
    user_response = create_user(
        username="andy is fake",
        password="randomPass",
        email="andysit174@gmail.com"
    )

    if user_response:
        print(user_response.model_dump_json(indent=4))

    # #TODO i dont think we ever nee "link", we can just auto generate base on the information when user wants to generate a qr.. code
        # side not we should make this auto, so we dont have manually add this...
    bin_create_obj = BinCreate(
        description="my second ever bin",
        bin_id="132",
        link="youtube.com",
        user_id="2"
    )

    bin_response = create_bin(bin_create_obj)
    if bin_response:
        print(bin_response.model_dump_json(indent=4))


