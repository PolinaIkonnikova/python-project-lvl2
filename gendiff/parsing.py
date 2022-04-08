import json
import yaml


def parsing_data(data, ending):
    try:
        if ending == '.yaml' or '.yml':
            data_dict = yaml.load(data, Loader=yaml.FullLoader)
        elif ending == '.json':
            data_dict = json.load(data)

        if data_dict is None:
            raise TypeError
    except (TypeError, yaml.parser.ParserError):
        return False
    else:
        return data_dict
