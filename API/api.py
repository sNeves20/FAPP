from os import stat, stat_result
import re

from bson.objectid import ObjectId
from pydantic.types import Json
from yaml import safe_dump
from models.schemas import SavingsBody, UserBase, BrokerUser
from typing import AnyStr, Optional
from fastapi import FastAPI, Header
from fastapi import security
from fastapi.params import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from utils.users import user_exists, create_new_user
from utils.savings import manage_savings, get_total_savings, Actions
from utils.securiry import hash_password, check_hash
from utils.stocks import add_broker_account, get_broker_information
from fastapi.responses import JSONResponse


app = FastAPI(title="Financial APPlication", version="0.0.1")
security = HTTPBasic()

SUPPORTED_BROKERS = ["etoro", "degiro"]


@app.get("/")
def base():
    return "<h1 Helcome to the Financial APP! (FAPP)/>"


# User Endpoints
@app.post("/user/signup")
async def register_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Returns the user ID that will be used to access all other endpoints"""

    username = credentials.username
    password = credentials.password

    user = await user_exists(UserBase(username=username, password=password))

    # Checking if user already exists
    if not user:
        await create_new_user(
            UserBase(username=username, password=hash_password(password))
        )
        return JSONResponse(
            {"message": f"Created successfully new user with username: {username}"},
            status_code=200,
        )

    return JSONResponse(
        {"error_message": "A user with that username already exists"}, status_code=400
    )


@app.get("/user/login")
async def login_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Returns the user ID, that will be used to access all other endpoints"""
    username = credentials.username
    password = credentials.password

    user_data = await user_exists(UserBase(username=username, password=password))

    if not user_data:
        return JSONResponse(
            {"error_message": "Could not verify user."}, status_code=403
        )

    if not check_hash(password, user_data["password"]):
        return JSONResponse(
            {"error_message": "Could not verify user."}, status_code=403
        )

    return JSONResponse({"user_id": str(user_data["_id"])}, status_code=200)


@app.post("/savings/editAmount")
async def edit_user_savings(savings_info: SavingsBody, userid: str = Header(None)):
    """Adds or removes value to savings according to bank location"""

    action = savings_info.action
    value = savings_info.amount
    location = savings_info.location

    if action is None or value is None:
        return JSONResponse(
            {"error_message": "The action and value are mandatory headers!"},
            status_code=400,
        )

    if not action in Actions.__members__:
        return JSONResponse(
            {
                "error_message": f"The action header needs to be one of the following: {Actions.__members__}"
            },
            status_code=400,
        )
    print(userid, action, value, location)
    try:
        results = await manage_savings(
            userid=userid, action=action, value=value, location=location
        )
        if results is False:
            return JSONResponse(
                {"error_message": "Could not add data to the database"}, status_code=500
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            {
                "error_message": "An error occurred while trying to edit savings",
                "full_error": f"{e}",
            },
            status_code=500,
        )

    if action == Actions.Add:
        message = ["added", "to"]
    elif action == Actions.Remove:
        message = ["removed", "from"]

    return JSONResponse(
        {"message": f"Successfuly {message[0]} {value}€ {message[1]} savings"},
        status_code=200,
    )


@app.get("/savings/getTotalAmount")
async def get_all_savings(userid: str = Header(None)):
    """Gets the total amount in savings"""
    userid = ObjectId(userid)
    return JSONResponse(
        {"message": f"{await get_total_savings(userid)}"}, status_code=200
    )


# Stock endpoints
@app.post("/stocks/brokers/addAccount")
async def sync_broker_account(userdata: BrokerUser, userid: str = Header(None)):
    """Adds a broker account to"""

    if userdata.broker_name.lower() not in SUPPORTED_BROKERS:
        return JSONResponse(
            {
                "message": f"The broker you are trying add is not supported. \n Try one of the following brokers: {SUPPORTED_BROKERS}"
            },
            status_code=400,
        )
    try:
        if await add_broker_account(userdata, userid=userid):
            return JSONResponse(
                {
                    "message": f"Successfully added a new {userdata.broker_name} broker account!"
                },
                status_code=200,
            )
    except Exception as e:
        return JSONResponse(
            {"message": "Failed to add a new broker account", "error": f"{e}"},
            status_code=500,
        )

    return JSONResponse(
        {"message": "Failed to add a new broker account"}, status_code=400
    )


@app.get("/stocks/brokers/getInfomation")
async def get_broker(broker: str = Header(None), userid: str = Header(None)):

    information = get_broker_information(userid, broker)

    return information
