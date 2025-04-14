from ..utils import reverse_mapping

user_batch_mapping = {
    "67fbe790993d093f6b3a9480" : ["67fbe9baa73a6a81e5e65b10", "67fbe9baa73a6a81e5e65b11"],  # Rishi Tiku - DS-2025, CA-2025-Odd
    "67fbe790993d093f6b3a9481" : ["67fbe9baa73a6a81e5e65b0f", "67fbe9baa73a6a81e5e65b11"],  # Arsh Raina - AIML-2025, CA-2025-Odd
}

batch_user_mapping = reverse_mapping(user_batch_mapping)


# batch_user_mapping = {
#     "67fbe9baa73a6a81e5e65b10": ["67fbe790993d093f6b3a9480"],
#     "67fbe9baa73a6a81e5e65b0f": ["67fbe790993d093f6b3a9481"], 
#     "67fbe9baa73a6a81e5e65b11": ["67fbe790993d093f6b3a9480", "67fbe790993d093f6b3a9481"],
# }