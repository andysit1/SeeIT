from typing import Union
from fastapi import FastAPI
from typing import Any

from models.user_model import UserIn, UserOut

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/send/{userid}-{binid}")
def get_qr(userid:int, binid: int):
    # called when frontend loads link to seeit
    # pull the json data for the bin, including
      # qr png code
      # description

    #MAKE FAKE QR CODE + DATA.. HERE
    return {"userid" : userid, "binid" : binid}

# Authentication ENDPOINTS, create fresh user.. with no bins
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user




#QR creator, ->