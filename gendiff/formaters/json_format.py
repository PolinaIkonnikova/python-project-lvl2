import json


def json_format(node_list):
    return json.dumps(node_list, indent=3, sort_keys=True)
