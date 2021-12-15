import re
from pymongo import mongo_client
from models.schemas import UserBase
from controller.mongo import MongoConnector


async def user_exists(userdata: UserBase):

    mongo = MongoConnector.connect_db_conf()

    user_data = mongo.search_by_username(userdata.username)
    mongo.close_connection()

    if user_data is not None:
        return user_data

    return False


async def create_new_user(user_data: UserBase):

    # Connect to the MongoDB
    mongo = MongoConnector.connect_db_conf()

    return mongo.add_user(user_data), mongo.close_connection()
