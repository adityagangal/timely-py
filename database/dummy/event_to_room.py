from ..utils import reverse_mapping

event_room_mapping = {
    "67fe113b5e58e1ca4c7804e5": ["6803c82eb3f66c2fceb01e6d"], # BDA - 407
    "67fe113b5e58e1ca4c7804e6": ["6803c82eb3f66c2fceb01e6c"], # NLP - 405
    "68052745b8797fefa1e7fa0e": ["68052c37760ab4fb49a72374"], # CA - 406-A
}

room_event_mapping = reverse_mapping(event_room_mapping)