""""
Init file of the controller module
Place here all the information that should be loaded
when accessing the controller module
"""

# pylint: disable=E0401

from abc import ABC, abstractmethod

from bson.objectid import ObjectId

from models.pydantic_schemas import UserData


class DataConnector(ABC):

    """Abstract base class to access and interact with the desired database"""

    @classmethod
    @abstractmethod
    def add_user(cls, user: UserData):
        """
        This function receives a the user info as a 'UserData' object
        and adds the user to the database
        """

    @classmethod
    @abstractmethod
    def edit_entry(cls, userid: ObjectId, query: dict):
        """This function shoudl be used to edit user information"""

    @classmethod
    @abstractmethod
    def search_by_username(cls, username: str):
        """This function will search the user by username"""

    @classmethod
    @abstractmethod
    def search_by_userid(cls, userid: ObjectId):
        """This function will search a user by user id"""

    @staticmethod
    @abstractmethod
    def connect_db_conf():
        """This function  will return an object"""
