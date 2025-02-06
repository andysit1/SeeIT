from typing import Union
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Any
from models.user_model import SignUpSchema, LoginUpSchema
import io
import pyqrcode
from fastapi.responses import HTMLResponse, JSONResponse
from components.database import UserResponse, UserCreate, BinResponse, BinCreate, create_user

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


"""
    Ideal keep the base static so I can just use github sites for MVP
    easy saving on costs and experimentation
"""


# @app.post('/new_user')


@app.post("/signup", response_model=UserResponse)
async def create_an_account(user: UserCreate):
    new_user = create_user(
        username=user.username,
        password=user.password,
        email=user.email
    )

    if new_user:
        return new_user
    else:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists."
        )

#requires permissions, next big implementation.
@app.post("/create_bin", response_class=BinResponse)
async def create_bin(bin: BinCreate):
    # new_bin =
    pass

@app.post("/login")
async def create_access_token(user_data: LoginUpSchema):
    pass


@app.get("/bin/{user_id}")
def get_user_bins(user_id : str):
    return {"user_id" : user_id}

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
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My FastAPI Page</title>
    </head>
    <body>
        <h1>Hello, FastAPI!</h1>
        <p>This is an example of returning HTML from a FastAPI route.</p>
    </body>
    </html>
    """
    return html_content


#This could be our social network aspect of the site..
#Can discover others in the world doing cool stuff

# @app.get("/discover", response_class=HTMLResponse)
# async def discover_other_impacts():
@app.get("/{user_id_slug}/{bin_id_slug}", response_class=HTMLResponse)
async def display_context(user_id_slug: str, bin_id_slug: str):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Send Data</title>
    </head>
    <body>
        <h1>Send Data for User {user_id_slug} and Bin {bin_id_slug}</h1>
        <form action="/send/{user_id_slug}/{bin_id_slug}" method="post">
            <label for="input_text">Enter Text:</label>
            <input type="text" id="input_text" name="input_text" required>
            <button type="submit">Send</button>
        </form>
    </body>
    </html>
    """
    return html_content

# Endpoint to receive form data and return it as JSON and save it
@app.post("/send/{user_id_slug}/{bin_id_slug}")
async def receive_data(user_id_slug: str, bin_id_slug: str, input_text: str = Form(...)):
    # Return the received context as JSON

    # do db interactions where..
    """
        grab the data from user/bin_id
            pull the media bucket or that specific model out of the data
            make it more extensible with better coding practices

        add the new media given type of medium + add a boolean if it's from a verified account
            will be used in the future when we want suspcious bin or good bin. (which is up to the user... later (implmentation))

        after making new entry, rewrite the data over the last "media" object.
            might need to check if this is good db practice
    """
    return JSONResponse(
        content={
            "user_id": user_id_slug,
            "bin_id": bin_id_slug,
            "input_text": input_text
        }
    )