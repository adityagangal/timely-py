from ..utils import prepare_objects

batch_keys = ["name", "code", "description",
            "subscribers", "admins", "events", "live_events"]

batches = [
    ["AIML 2025", "AIML-2025", "All AIML 2025 passout students", [], [], [], []],
    ["DS 2025", "DS-2025", "All DS 2025 passout students", [], [], [], []],
    ["CA 2025 Odd", "CA-2025-Odd", "CA 2025 students for Odd Semester", [], [], [], []]
]

def get_batch_objects():
    return prepare_objects(batch_keys, batches)

if __name__ == "__main__":
    print(*get_batch_objects(), sep="\n")