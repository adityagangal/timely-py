from ..utils import prepare_objects

room_keys = ["code", "events"]

rooms = [["404", []], ["405", []], ["407", []], ["409", []]]

def get_room_objects():
    return prepare_objects(room_keys, rooms)





