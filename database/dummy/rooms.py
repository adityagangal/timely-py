from ..utils import prepare_objects

room_keys = ["code", "events"]

# rooms = [["404", []], ["405", []], ["407", []], ["409", []]]

rooms = [["406-A", []], ["406-B", []]]

def get_room_objects():
    return prepare_objects(room_keys, rooms)





