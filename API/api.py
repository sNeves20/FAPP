from models.schemas import UserBase
from typing import Optional
from fastapi import FastAPI, Header
from fastapi import security
from fastapi.params import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from utils.users import user_exists, create_new_user
import uvicorn
from utils.securiry import hash_password, check_hash
from fastapi.responses import JSONResponse



app = FastAPI()
security = HTTPBasic()

@app.get("/")
def base():
    return "<h1 Helcome to the Financial APP! (FAPP)/>"


# User Endpoints
@app.post("/user/signup")
async def register_user(credentials: HTTPBasicCredentials = Depends(security) ):
    """Returns the user ID that will be used to access all other endpoints"""
    
    username = credentials.username
    password = credentials.password

    user = await user_exists(UserBase(username=username, password=password))

    # Checking if user already exists 
    if not user:
        await create_new_user(UserBase(username=username, password=hash_password(password)))
        return JSONResponse({f"Created successfully new user with username: {username}"}, status_code=200)

    return JSONResponse({"A user with that username already exists"}, status_code=400)

@app.get("/user/login")
async def login_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Returns the user ID, that will be used to access all other endpoints"""
    username = credentials.username
    password = credentials.password

    user_data = await user_exists(UserBase(username=username, password=password))

    if not user_data: 
        return JSONResponse({"Could not verify user."}, status_code=403)

    if not check_hash(password, user_data["password"]):
        return JSONResponse({"Could not verify user."}, status_code=403)

    return JSONResponse({'user_id': str(user_data['_id'])}, status_code=200)

@app.get("/savings")
async def edit_user_savings(action: Optional[str] = Header(None), value: Optional[float] = Header(None)):

    valid_actions = ["add", "remove"]

    if action is None or value is None:
        return JSONResponse({"error_message" : "The action and value are mandatory headers!"}, status_code=400)
    
    if not action in valid_actions:
        return JSONResponse({"error_message": f"The action header needs to be one of the following: {valid_actions}"}, status_code=400)

    return JSONResponse({"message": f"Successfuly {action}ed {value}€ from savings"}, status_code=200)