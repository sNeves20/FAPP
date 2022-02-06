""" Module in charge of handling the various user related requests """
# pylint: disable=E0401
from models.pydantic_schemas import UserBase
from controller.mongo import MongoConnector


async def user_exists(userdata: UserBase):
    """Function that will check if a user exists in the database"""

    mongo = MongoConnector.connect_db_conf()

    user_data = mongo.search_by_username(userdata.username)
    mongo.close_connection()

    if user_data is not None:
        return user_data

    return False


async def create_new_user(user_data: UserBase):
    """Function that will create a new user"""
    # Connect to the MongoDB
    mongo = MongoConnector.connect_db_conf()

    return mongo.add_user(user_data), mongo.close_connection()
