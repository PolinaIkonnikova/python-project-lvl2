import json
import yaml


def pars(file_data, ending):
    if ending == '.yaml' or '.yml':
        return yaml.load(file_data, Loader=yaml.FullLoader)
    if ending == '.json':
        return json.load(file_data)
