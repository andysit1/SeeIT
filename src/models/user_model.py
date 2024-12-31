
#all users have an id, bin list (storage representation)
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


#LOGIN
class SignUpSchema(BaseModel):
    username: str
    password: str

class LoginUpSchema(BaseModel):
    email: str
    password: str