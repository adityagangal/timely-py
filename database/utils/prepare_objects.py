from typing import List
def prepare_objects(keys, data):
    return [dict(zip(keys, entry)) for entry in data]
def reverse_mapping(mapping: dict[str, List[str]]):
    rev_mapping = {}
    for key, values in mapping:
        for v in values:
            if v in rev_mapping:
                rev_mapping[v].append(key)
            else:
                rev_mapping[v] = [key]
    return rev_mapping
