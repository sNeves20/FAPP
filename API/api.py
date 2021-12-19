"""
                Financial APPlication: API
    Entry point of the backend of the Financial Application API
"""
# pylint: disable=E0602

import logging
from datetime import datetime
from bson.objectid import ObjectId
from fastapi import FastAPI, Header
from fastapi.params import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi.responses import JSONResponse
from utils.users import user_exists, create_new_user
from utils.savings import manage_savings, get_total_savings, Actions
from utils.securiry import hash_password, check_hash
from utils.stocks import (
    add_broker_account,
    SupportedBrokers,
    get_portfolio_data,
)
from models.pydantic_schemas import SavingsBody, UserBase, BrokerUser


app = FastAPI(title="Financial APPlication", version="0.0.1")
security = HTTPBasic()

logging.basicConfig()

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

    action = savings_info.action.lower()
    value = savings_info.amount
    location = savings_info.location

    # Checking body information
    if (
        action is None
        or (value is None or value < 0)
        or not action in Actions.__members__
    ):
        return JSONResponse(
            {
                "error_message": "There is information missing in your request. "
                "\n Please verify that your request has the correct: action and value"
            },
            status_code=400,
        )

    # Editing data in the Database
    try:
        results = await manage_savings(
            userid=userid, action=action, value=value, location=location
        )
        if results is False:
            return JSONResponse(
                {"error_message": "Could not add data to the database"}, status_code=500
            )
    except AssertionError as edit_error:
        return JSONResponse(
            {
                "error_message": "An error occurred while trying to edit savings",
                "full_error": edit_error,
            },
            status_code=500,
        )

    if action == Actions.add.name:
        message = ["added", "to"]
    elif action == Actions.remove.name:
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
    """Adds a broker account to the user account"""

    if userdata.broker_name.lower() not in SupportedBrokers.__members__:
        return JSONResponse(
            {
                "message": "The broker you are trying add is not supported."
                f"\n Try one of the following brokers: {SUPPORTED_BROKERS}"
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
    except NameError as name_error:
        return JSONResponse(
            {"message": "Failed to add a new broker account", "error": f"{name_error}"},
            status_code=500,
        )

    return JSONResponse(
        {"message": "Failed to add a new broker account"}, status_code=400
    )


@app.get("/stocks/brokers/getPortfolio")
async def get_portfolio(broker: str = Header(None), userid: str = Header(None)):
    """Endpoint that receives data from the given broker"""
    broker = broker.lower()

    portfolio_data = await get_portfolio_data(userid=userid, broker_name=broker)

    if "error" in portfolio_data.keys():
        return JSONResponse({"message": portfolio_data["error"]}, status_code=404)

    return JSONResponse({"message": portfolio_data}, status_code=200)
