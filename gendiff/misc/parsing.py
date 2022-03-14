import json
import yaml


def pars_yaml(pathfile):
    with open(pathfile) as f:
        read_data = yaml.load(f, Loader=yaml.FullLoader)
    return read_data


def pars_json(pathfile):
    return json.load(open(pathfile))
