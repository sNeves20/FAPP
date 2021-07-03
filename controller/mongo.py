from genericpath import exists

from pymongo.operations import InsertOne
from models.schemas import UserData
from pymongo import MongoClient, collation, collection

ERROR_MESSAGE = "ERROR; MongoConnector"

class MongoConnector:

    def __init__(self, mongo_host:str, mongo_port:int = None):
        
        self.db = None
        self.collection = None 

        try:
            if mongo_port is not None:
                self.client = MongoClient(mongo_host, port=mongo_port)
            else:
                self.client = MongoClient(mongo_host)
        except Exception as e:
            raise e
        
    def connect_to_database(self, database_name:str, collection_name: str):
        
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
                    
    def add_entry(self, json_data: UserData):

        try:
            self.collection.insert(json_data.json())
        except Exception as e:

            print(f"{ERROR_MESSAGE}: Error Adding entry \n \t {e}")

