import json
import yaml


def parsing_data(file_data, ending):
    if ending == '.yaml' or '.yml':
        data_dict = yaml.load(file_data, Loader=yaml.FullLoader)
    elif ending == '.json':
        data_dict = json.load(file_data)
    if data_dict is None:
        return {}
    return data_dict
