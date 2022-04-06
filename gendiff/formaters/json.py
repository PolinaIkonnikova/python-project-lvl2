import json


def make_format(diff_dict):
    return json.dumps(diff_dict, indent=3, sort_keys=True)
