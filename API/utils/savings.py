from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from API.models.schemas import UserData
from controller.mongo import MongoConnector
from logging import Logger, INFO, DEBUG
from enum import Enum, auto


class Actions(Enum):
    """Enum for the available action we can execute on savings"""

    add = auto()
    remove = auto()


# Savings
async def manage_savings(
    action: str, value: float, userid, location: str = "None"
) -> bool:

    # Connecting to a DB
    mongo = MongoConnector.connect_db_conf()

    savings_list = []
    current_savings = 0
    try:
        savings_list = mongo.search_by_userid(userid=userid)["savings"]
    except Exception as e:
        current_savings = 0

    # Looking for savings id
    savings_id = -1
    new_savings = 0
    for i in range(len(savings_list)):
        savings = savings_list[i]
        if savings["location"] == location.lower():
            savings_id = i
            break
    # Returning if we try to remove from non existing savings
    if savings_id == -1 and action == Actions.remove.name:
        return False
    # Getting current savings
    elif savings_id != -1:
        current_savings = savings_list[savings_id]["value"]
        if action == Actions.remove and value > float(current_savings):
            raise AssertionError(
                "Problem removing savings, value is probably larger than the amount in savings."
            )
        elif action == Actions.remove.name:
            new_savings = float(current_savings) - float(value)
        elif action == Actions.add.name:
            new_savings = float(current_savings) + float(value)

        savings_list[savings_id]["value"] = new_savings

        if new_savings == 0:
            savings_list.pop(savings_id)
    # If location still does not exist, add it
    else:
        savings_list.append({"value": value, "location": location.lower()})

    results = mongo.edit_entry(userid=userid, query={"$set": {"savings": savings_list}})

    return results


async def get_total_savings(userid: ObjectId) -> float:

    mongo = MongoConnector.connect_db_conf()

    savings_list = mongo.search_by_userid(userid)["savings"]

    total = 0
    for item in savings_list:

        total += item["value"]

    return total
