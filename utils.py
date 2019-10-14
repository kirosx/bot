from bson import ObjectId
from bson.objectid import InvalidId


def obj_id_checker(some_id: str):
    try:
        ObjectId(some_id)
    except InvalidId:
        return False
    return True


def buy_button_checker(input_string: str):
    split_string = input_string.split()
    return True if len(split_string) == 2 and split_string[0] == 'buy' and obj_id_checker(split_string[1]) else False
