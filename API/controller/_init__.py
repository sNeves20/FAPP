from abc import ABC, abstractmethod

from bson.objectid import ObjectId

from models.schemas import UserData

class DataConnector(ABC):

    @abstractmethod
    @classmethod
    def add_user(self, user: UserData):
        pass

    @abstractmethod
    @classmethod
    def edit_entry(self, userid: ObjectId, query: dict):
        pass

    @abstractmethod
    @classmethod
    def search_by_username(self, username: str):
        pass

    @abstractmethod
    @classmethod
    def search_by_userid(self, userid):
        pass

    @abstractmethod
    @staticmethod
    def connect_db_conf():
        pass