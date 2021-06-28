from models.schemas import UserBase
from fastapi import FastAPI
from fastapi import security
from fastapi.params import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from utils.users import user_exists, create_new_user

app = FastAPI()
security = HTTPBasic()

@app.get("/")
def base():
    return "<h1 Helcome to the Financial APP (FAPP)/>"


@app.post("/user/signup")
async def register_user(credentials: HTTPBasicCredentials = Depends(security) ):
    
    username = credentials.username
    password = credentials.password

    # Checking if user already exists 
    if user_exists(UserBase(username, password)):

        return 400, "A user with that username already exists"
    
    create_new_user(UserBase(username, password))

    return 

    

    