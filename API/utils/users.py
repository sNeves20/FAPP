import configparser
import re
from pymongo import mongo_client
from models.schemas import UserBase
from controller.mongo import MongoConnector
import yaml


# Loading from config file
with open('configs/mongo.yml') as config_file:
     config = yaml.load(config_file, Loader=yaml.FullLoader)



MONGO_HOST = config['dev']['host']
MONGO_PORT = config['dev']['port']
DATABASE = config['dev']['database']
COLLECTION = config['dev']['collection']

def connect_db():
    mongo = MongoConnector(mongo_host = MONGO_HOST, mongo_port = MONGO_PORT)
    mongo.connect_to_database(database_name=DATABASE, collection_name=COLLECTION)
    return mongo

async def user_exists(userdata: UserBase):

    mongo = connect_db()
    
    if mongo.search_by_username(userdata.username) is not None:
        return True

    return False

async def create_new_user(user_data: UserBase):

    # Connect to the MongoDB
    mongo = connect_db()

    return mongo.add_entry(user_data), mongo.close_connection()



if __name__ == "__main__":
    create_new_user(UserBase(username="Test", password="testpassword"))
