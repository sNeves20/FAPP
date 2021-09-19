from brokers import Broker
import degiroapi


class DegiroBroker(Broker):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.degiro = degiroapi.DeGiro()

    def login(self):

        self.degiro.login(self.username, self.password)

    def logout(self):

        self.degiro.logout()

    def get_portfolio(self):

        portfolio = degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
