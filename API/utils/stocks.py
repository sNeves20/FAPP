from logging import exception
from bson.objectid import ObjectId
from fastapi.param_functions import Query
from utils.users import user_exists
from controller.mongo import MongoConnector
from pymongo import mongo_client
from models.schemas import BrokerUser


async def add_broker_account(user: BrokerUser, userid: ObjectId) -> bool:

    mongo = MongoConnector.connect_db_conf()

    try:
        query = mongo.search_by_userid(userid=userid)
    except Exception as e:
        print(f"\t ERROR in acessingDB {__name__}! Full error {e}")
        return False

    # Setting Broker list
    try:
        if query != None:
            broker_list = query["brokers"]
    except:
        broker_list = []

    if broker_list:
        for broker in broker_list:
            if broker["broker"] == BrokerUser.broker_name:
                raise Exception(
                    f"There is already a broker account saved for {BrokerUser.broker_name}"
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
    except Exception as e:
        print(f"{e}")
        return False
    return results


async def get_broker_information(userid: ObjectId, broker: str) -> dict:

    mongo = MongoConnector.connect_db_conf()

    try:
        query = mongo.search_by_userid(userid=userid)
    except Exception as e:
        print(f"\t ERROR in accessing database {__name__}! Full error {e}")

    if query != None:
        brokers = query["broker"]

    for broker_info in brokers:
        if broker_info["broker"] == broker:
            return broker_info

    return None
