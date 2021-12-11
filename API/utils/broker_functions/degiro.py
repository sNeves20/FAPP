from utils.broker_functions import Broker
import degiroapi


class DegiroBroker(Broker):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.degiro = degiroapi.DeGiro()

    async def login(self):

        self.degiro.login(username=self.username, password=self.password)

    async def logout(self):

        self.degiro.logout()

    async def get_portfolio(self) -> list:

        await self.login()
        raw_stock_data = self.degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
        await self.logout()

        return raw_stock_data

    async def get_product_name(self, product_id: str) -> str:
        await self.login()
        product_name = self.degiro.product_info(product_id)["name"]
        await self.logout()

        return product_name

    async def filter_stock_data(self, stock_data: list) -> dict:

        cash_data = [item for item in stock_data if item["positionType"] == "CASH"]

        product_data = [
            item for item in stock_data if item["positionType"] == "PRODUCT"
        ]

        p_names = [await self.get_product_name(i["id"]) for i in product_data]

        for i in range(len(product_data)):
            product_data[i]["product_name"] = p_names[i]

        organized_data = {"Cash": cash_data, "Product": product_data}

        return organized_data
