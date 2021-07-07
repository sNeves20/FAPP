from genericpath import exists
import json
from pymongo.operations import InsertOne
from models.schemas import UserData
from pymongo import MongoClient, collation, collection

ERROR_MESSAGE = "ERROR; MongoConnector"

class MongoConnector:

    def __init__(self, mongo_host:str, mongo_port:int = None):
        
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
        except Exception as e :
            raise e

    def connect_to_database(self, database_name:str, collection_name: str) -> False:

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
            print (f"{ERROR_MESSAGE}: Error connecting to Database \n\t {e}")    
            return False

        return True


    def add_entry(self, data: UserData) -> bool:
        """
        Method that adds a user to the database

        :returns bool: Returns true if user was added to DB and false if it was not
        """
        json_data = data.dict()
        print(json_data)
        try:
            self.collection.insert(json_data)
        except Exception as e:

            print(f"{ERROR_MESSAGE}: Error Adding entry \n \t {e}")
            return False
        
        return True

    def search_by_username(self, username:str) -> dict:

        user = self.collection.find_one({"username": username})
        

        return user

    def search_by_uuid(self, uuid) -> dict:
        
        user = self.collection.find(f"")