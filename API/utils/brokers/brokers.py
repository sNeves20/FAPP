from abc import abstractmethod, ABC


class Broker(ABC):
    def __init__(self, username, password):

        self.username = username
        self.password = password

    @abstractmethod
    def login(self):
        """This method is in charge of logging in the
        user into their broker account"""
        pass

    @abstractmethod
    def logout(self):
        """This method is in charge of logging the
        user out of their broker account"""
        pass

    @abstractmethod
    def get_portfolio(self):
        """This method is in charge of getting
        the users' portfolio"""
        pass
