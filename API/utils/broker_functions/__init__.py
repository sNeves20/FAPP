"""Module that provides the functionality to create and handle broker information"""
from abc import abstractmethod, ABC


class Broker(ABC):
    """Base of the Broker class all broker objects should inherite from this class"""
    def __init__(self, username, password):

        self.username = str(username)
        self.password = str(password)

    @abstractmethod
    def login(self):
        """This method is in charge of logging in the
        user into their broker account"""

    @abstractmethod
    def logout(self):
        """This method is in charge of logging the
        user out of their broker account"""

    @abstractmethod
    def get_portfolio(self):
        """This method is in charge of getting
        the users' portfolio"""
