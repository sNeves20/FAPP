from models.schemas import UserData
from controller.mongo import MongoConnector

async def manage_savings(action: str, value: float, userid) -> bool:

    # Connecting to a DB
    mongo = MongoConnector.connect_db_conf()

    current_savings = mongo.search_by_userid(userid=userid)['savings']

    if action == 'remove' and (current_savings is None or value > current_savings):
        raise "Problem removing savings, value is probably too large"

    if action == 'remove':
        new_savings = float(current_savings) - float(value)
    else:
        new_savings = float(current_savings) + float(value)

    return mongo.edit_entry(userid=userid, query={"$set": {"savings": f"{new_savings}"}})
