from ..utils import reverse_mapping

batch_event_mapping = {
        "67fbe9baa73a6a81e5e65b0f" : ["67fcf4b5bf4e66c4fc5e9f93"],
        # "code": "AIML-2025",
        "67fbe9baa73a6a81e5e65b10" : ["67fcf4b5bf4e66c4fc5e9f92"],
        # "code": "DS-2025",
        "67fbe9baa73a6a81e5e65b11" : ["67fcf4b5bf4e66c4fc5e9f94"],
        # "code": "CA-2025-Odd",
}

event_batch_mapping = reverse_mapping(batch_event_mapping)