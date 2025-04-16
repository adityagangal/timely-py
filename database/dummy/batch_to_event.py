from ..utils import reverse_mapping

batch_event_mapping = {
        "67fbe9baa73a6a81e5e65b0f" : ["67fe113b5e58e1ca4c7804e6"],
        # "code": "AIML-2025",
        "67fbe9baa73a6a81e5e65b10" : ["67fe113b5e58e1ca4c7804e5"],
        # "code": "DS-2025",
        "67fbe9baa73a6a81e5e65b11" : ["67fe113b5e58e1ca4c7804e7"],
        # "code": "CA-2025-Odd",
}

event_batch_mapping = reverse_mapping(batch_event_mapping)
