from fastapi import FastAPI, HTTPException

from src2.db.DBManager import DatabaseManager
from src2.db.UserModels import User, UserResponse, UserCreate, Media, MediaCreate, Bin, BinCreate
from src2.util import generate_bin_id
app = FastAPI()
database_url = "sqlite:///test.db"
db_manager = DatabaseManager(database_url)

#uvicorn src2.main:app --reload -> can run server like this so that it knows we're in the src2 "dir"...


@app.post("/post/bin/")
async def post_bin( bin_create : BinCreate):
    bin_id = generate_bin_id()
    new_bin = Bin(
        user_id = bin_create.user_id,
        bin_id=bin_id,
        description=bin_create.description,
        media_items=[]
    )

    if db_manager.add(new_bin):
        try:
            return db_manager.query_first(Bin, {"bin_id": bin_id})
        except Exception as e:
            print(f"Error found in post_bin: {e}")
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Bin with bin_id {bin_id} does not exists"
        )

#user based routes...
@app.post("/post/media/{bin_id}")
async def post_media(bin_id: str, media: MediaCreate):
    new_media = Media(bin_id=bin_id, content=media.content, type=0)
    if db_manager.add(new_media):
        try:
            return db_manager.query_first(Media, {"bin_id": bin_id})
        except Exception as e:
            print(f"Error found in post_media: {e}")
    else:
        raise HTTPException(
            status_code=409,
            detail="Media with bin_id does not exists"
        )

@app.post("/signup", response_model=UserResponse)
async def create_an_account(user: UserCreate):
    new_user = User(username=user.username, password=user.password, email=user.email)
    if db_manager.add(new_user):
        #not sure if this is effi. i think when i called new_user before by reusing it would cause an error since my session would have closed then..
        return db_manager.query_first(User, {"username": user.username})
    else:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists."
        )

@app.get("/get_user_by_username/{username_slug}", response_model=UserResponse)
async def get_user_by_username(username_slug : str):    # db_manager.add(new_user)
    user_response = db_manager.query_first(User, {"username": username_slug})
    return user_response


@app.get("/get_user_by_id/{user_id_slug}", response_model=UserResponse)
async def get_user_by_id(user_id_slug : int):    # db_manager.add(new_user)
    user_response = db_manager.query_first(User, {"id": user_id_slug})
    return user_response


@app.get("/")
async def root():    # db_manager.add(new_user)
    user_response = db_manager.query_first(User, {"username": "Alice2"})
    return user_response




