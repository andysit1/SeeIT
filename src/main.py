from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import Any
from models.user_model import SignUpSchema, LoginUpSchema
import io
import pyqrcode

app = FastAPI()

# For Firebase JS SDK v7.20.0 and later, measurementId is optional
firebaseConfig = {
  "apiKey": "AIzaSyA924JobIg__WmuoWcAs9mMsq93gpIJ7t4",
  "authDomain": "seeit-3671b.firebaseapp.com",
  "projectId": "seeit-3671b",
  "storageBucket": "seeit-3671b.firebasestorage.app",
  "messagingSenderId": "755805630816",
  "appId": "1:755805630816:web:cd14e922f60cfd998dae05",
  "measurementId": "G-K0KJGY8WZ6",
  "databaseURL": ""
};


@app.post("/signup")
async def create_an_account(user_data: SignUpSchema):
    pass

@app.post("/login")
async def create_access_token(user_data: LoginUpSchema):
    pass

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/bin/{user_id}")
def get_user_bins(user_id : str):
    return {"user_id" : user_id}

@app.get("/send")
def dump_media():
    return {"msg": "hello world"}

# example of returning qr code...
# used when user wants to start using their qr code.
# only used in the dashboard when applicable.
@app.get("/qrcode")
def generate_qrcode(data: str):
    qr_code = pyqrcode.create(data)
    buffer = io.BytesIO()
    qr_code.png(buffer, scale=5)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

#QR creator, ->