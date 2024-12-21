from pydantic import BaseModel, Field
from typing import List, Optional

# All media objects need a timestamp
class Media(BaseModel):
    date: str

# Decorators deal with changes in data types and structure
class MediaDecorator(Media):
    wrap_media: Optional[Media] = Field(None, description="Wrapped media object")

class TextMediaDecorator(MediaDecorator):
    txt_content: str = Field(..., description="Text content for the media")

class ImageMediaDecorator(MediaDecorator):
    image_content: str = Field(..., description="Image content for the media")

# Holds media, description, link
class BinModel(BaseModel):
    description: str
    bin_id: int
    link: str
    bin_content: List[Media]

# Testing the flow of models
if __name__ == "__main__":
    print("Testing flow of models")

    # Create a basic Media instance (change base on given data)
    note = Media(date="Today")
    print("Original Media:", note)

    # Wrap it with a TextMediaDecorator
    text_decorator = TextMediaDecorator(wrap_media=note, date=note.date, txt_content="Hello")
    print("TextMediaDecorator:", text_decorator)

    # Wrap it with an ImageMediaDecorator
    image_decorator = ImageMediaDecorator(
        wrap_media=text_decorator, date=text_decorator.date, image_content="image.png"
    )
    print("ImageMediaDecorator:", image_decorator)
