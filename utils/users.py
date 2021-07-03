import configparser
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


async def user_exists(userdata: UserBase):

    # TODO: Query  the Database
    print("\tStill need to implement this")

    return

async def create_new_user(user_data: UserBase):

    # Connect to the MongoDB
    mongo = MongoConnector(mongo_host = MONGO_HOST, mongo_port = MONGO_PORT)
    mongo.connect_to_database(database_name=DATABASE, collection_name=COLLECTION)





if __name__ == "__main__":
    create_new_user(UserBase(username="Test", password="testpassword"))
