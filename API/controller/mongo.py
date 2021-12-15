"""
    MongoConnector Class
    This class is in charge of connecting to a Mongo Database in order to
    access data  
"""
from genericpath import exists
from pymongo.operations import InsertOne
from models.schemas import UserData
from pymongo import MongoClient, collection
from bson.objectid import ObjectId
import yaml
from bson.objectid import ObjectId
from controller import DataConnector


ERROR_MESSAGE = "ERROR; MongoConnector"


class MongoConnector(DataConnector):
    def __init__(self, mongo_host: str, mongo_port: int = None):

        self.db = None
        self.collection = None

        self.open_connection(mongo_port=mongo_port, mongo_host=mongo_host)

    def open_connection(self, mongo_host, mongo_port):
        try:
            if mongo_port is not None:
                self.client = MongoClient(mongo_host, port=mongo_port)
            else:
                self.client = MongoClient(mongo_host)
        except Exception as e:
            raise e

    def close_connection(self):

        try:
            self.client.close()
        except Exception as e:
            raise e

    def connect_to_database(self, database_name: str, collection_name: str) -> False:

        """
        Connects to a Mongo database

        :args database_name: The name of the MongoDB database
        :args collection_name: The name of the MongoDB collection

        :returns bool: True if connection to DB was successful and False if it was not
        """
        try:
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
        except Exception as e:
            print(f"{ERROR_MESSAGE}: Error connecting to Database \n\t {e}")
            return False

        return True

    def add_user(self, user: UserData) -> bool:
        """
        Method that adds a user to the database
        :params user: User data to be added
        :returns bool: Returns true if user was added to DB and false if it was not
        """
        json_data = user.dict()
        print(json_data)
        try:
            self.collection.insert(json_data)
        except Exception as e:

            print(f"{ERROR_MESSAGE}: Error Adding entry \n \t {e}")
            return False

        return True

    def edit_entry(self, userid: ObjectId, query: dict) -> bool:
        """
        Method that edits the data of a certain userid

        :param userid: The userid of the user that we will edit the information for
        :param query: The query that we will make to edit the data

        :return bool Returns True if the userdata was successfully edited
        """

        try:
            results = self.collection.find_one_and_update(
                {"_id": ObjectId(userid)}, query
            )
        except:
            raise Exception("Error updating user entry")
        if results is None:
            return False

        return True

    def search_by_username(self, username: str) -> dict:

        user = self.collection.find_one({"username": username})

        return user

    def search_by_userid(self, userid) -> dict:
        """
        Gets all of the user infor
        """

        user = self.collection.find_one({"_id": ObjectId(userid)})

        return user

    @staticmethod
    def connect_db_conf():
        # Loading from config file
        with open("configs/mongo.yml") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)

        MONGO_HOST = config["dev"]["host"]
        MONGO_PORT = config["dev"]["port"]
        DATABASE = config["dev"]["database"]
        COLLECTION = config["dev"]["collection"]

        mongo = MongoConnector(mongo_host=MONGO_HOST, mongo_port=MONGO_PORT)
        mongo.connect_to_database(database_name=DATABASE, collection_name=COLLECTION)

        return mongo
