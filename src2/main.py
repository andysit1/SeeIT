from fastapi import FastAPI

from src2.db.DBManager import DatabaseManager
from src2.db.UserModels import User, UserResponse

app = FastAPI()
database_url = "sqlite:///test.db"
db_manager = DatabaseManager(database_url)

#uvicorn src2.main:app --reload -> can run server like this so that it knows we're in the src2 "dir"...




@app.get("/")
async def root():    # db_manager.add(new_user)
    user_response = db_manager.query_first(User, {"username": "Alice2"})
    print(user_response)
    return user_response




