
#all users have an id, bin list (storage representation)
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


#LOGIN
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

#GUEST
class GuestUserIn(BaseModel):
    email: EmailStr
    full_name: str | None = None

