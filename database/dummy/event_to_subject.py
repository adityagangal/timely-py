from ..utils import reverse_mapping

event_subject_mapping = {
    "67fe113b5e58e1ca4c7804e5": ["68052745b8797fefa1e7fa0c"], # BDA
    "67fe113b5e58e1ca4c7804e6": ["68052745b8797fefa1e7fa0d"], # NLP
    "68052745b8797fefa1e7fa0e": ["68052745b8797fefa1e7fa0e"], # CA
}

subject_event_mapping = reverse_mapping(event_subject_mapping)