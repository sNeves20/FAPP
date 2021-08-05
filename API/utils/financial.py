from models.schemas import UserData
from controller.mongo import MongoConnector

async def manage_savings(action: str, value: float, userid, location: str = None) -> bool:

    # Connecting to a DB
    mongo = MongoConnector.connect_db_conf()

    try:
        current_savings = mongo.search_by_userid(userid=userid)['savings']
    except Exception as e:
    
        current_savings = 0
    
    if (action == 'remove' and value > current_savings):
        raise "Problem removing savings, value is probably larger than the amount in savings."

    if action == 'remove':
        new_savings = float(current_savings) - float(value)
    else:
        new_savings = float(current_savings) + float(value)

    results = mongo.edit_entry(userid=userid, query={"$set": {"savings": f"{new_savings}", "location": f"{location}"}})

    return results
