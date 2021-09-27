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
    

    def get_portfolio(self) -> list:

        raw_stock_data = degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)

        return organized_data(filter_stock_data(raw_stock_data))
        

    @static_method
    def filter_stock_data(stock_data: list) -> dict:
        
        cash_data = [item for item in stock_data if item['positionType']=='CASH']
        
        product_data = [item for item in stock_data if item['postionType']=='PRODUCT']

        organized_data = {"Cash": cash_data, "Product": product_data}
        
        return organized_data
