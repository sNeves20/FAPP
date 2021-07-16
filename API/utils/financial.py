from models.schemas import UserData
from controller.mongo import MongoConnector
from bson.objectid import ObjectId

async def manage_savings(action: str, value: float, userid):

    # Connecting to a DB
    mongo = MongoConnector.connect_db_conf()

    mongo.
