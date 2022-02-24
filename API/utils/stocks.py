"""
    Module in charge of stock handeling.
    At the moment we are simply using a
"""
# pylint: disable=E0401

from bson.objectid import ObjectId
from controller.mongo import MongoConnector
from models.pydantic_schemas import BrokerUser
from enum import Enum, auto
from utils.broker_functions.degiro import DegiroBroker


class SupportedBrokers(Enum):
    """List of Supported Brokers"""

    DEGIRO = auto()
    ETORO = auto()


# TODO: This needs to be deprecated, it should be done with
# session cookies and not adding this info to the database
async def add_broker_account(user: BrokerUser, userid: ObjectId) -> bool:
    """Function that adds a new broker account to the Database"""

    mongo = MongoConnector.connect_db_conf()

    try:
        query = mongo.search_by_userid(userid=userid)
    except Exception as access_error:
        print(f"\t ERROR in acessingDB {__name__}! Full error {access_error}")
        return False

    # Setting Broker list
    try:
        if query is not None:
            broker_list = query["brokers"]
    except:
        broker_list = []

    if broker_list:
        for broker in broker_list:
            if broker["broker"] == user.broker_name:
                print("\t This broker is already registered")
                raise NameError(
                    f"There is already a broker account saved for {user.broker_name}"
                )
    broker_list.append(
        {
            "broker": user.broker_name.lower(),
            "broker_username": user.username,
            "broker_password": user.password,
        }
    )
    try:
        results = mongo.edit_entry(
            userid=userid, query={"$set": {"brokers": broker_list}}
        )
    except Exception as access_error:
        print(f"{access_error}")
        return False
    return results


# TODO: This should be deprecated and start getting this info from set cookies
async def get_broker_information(userid: ObjectId, broker: str) -> dict:
    """Function that gets the broker information from the DB"""
    mongo = MongoConnector.connect_db_conf()

    try:
        query = mongo.search_by_userid(userid=userid)
    except Exception as access_error:
        print(f"\t ERROR in accessing database {__name__}! Full error {access_error}")

    if query != None:
        try:
            brokers = query["brokers"]
        except:
            return {
                "error": 404,
                "message": "This user does not contain any broker info",
            }

    for broker_info in brokers:
        if broker_info["broker"] == broker:
            return broker_info

    return {
        "error": 404,
        "message": f"This user has not registered any information about the {broker} broker",
    }


async def get_portfolio_data(userid: ObjectId, broker_name: SupportedBrokers) -> dict:

    mongo = MongoConnector.connect_db_conf()

    try:
        query = mongo.search_by_userid(userid=userid)
    except Exception as e:
        print(f"\t ERROR in accessing database {__name__}! Full error {e}")

    # Return message in case the user has no brokers associated
    if query == None:
        return {"error": "No user exists with that user_id"}
    try:
        brokers = query["brokers"]
    except:
        return {"error": "This user does not contain any broker information"}

    if broker_name == SupportedBrokers.DEGIRO.name:
        degiro_info = [b for b in brokers if b["broker"] == "degiro"][0]
        broker = DegiroBroker(
            degiro_info["broker_username"], degiro_info["broker_password"]
        )
        data = await broker.filter_stock_data(await broker.get_portfolio())
        return data
    return {"error": "This user has no information regarding the given broker"}
