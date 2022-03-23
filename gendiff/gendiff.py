from .parsing import pars
from .formaters.stylish import stylish
from .formaters.plain import plain
from .formaters.json_format import json_format


def get_value(val):
    js_values = {'True': 'true', 'False': 'false', 'None': 'null'}
    if isinstance(val, dict):
        return {k: get_value(v) for k, v in val.items()}
    val = str(val)
    if val in js_values:
        return js_values[val]
    return val


def make_diff(node1, node2):
    diff_dict = {}

    deleted_items = {key: {'value': get_value(node1[key]), 'type': 'deleted'}
                     for key in set(node1).difference(set(node2))}

    added_items = {key: {'value': get_value(node2[key]), 'type': 'added'}
                   for key in set(node2).difference(set(node1))}

    unchanged_items = {key: {
                       'value': get_value(node1[key]),
                       'type': 'unchanged'}
                       for key in set(node1).intersection(set(node2))
                       if node1[key] == node2[key]}

    changed_items = {key: {'value': [get_value(node1[key]),
                     get_value(node2[key])], 'type': 'changed_value'}
                     for key in set(node1).intersection(set(node2))
                     if node1[key] != node2[key] and (
                     not(isinstance(node1[key], dict)) or not(isinstance(
                                                              node2[key],
                                                              dict)))}

    changed_items_with_dicts = {key: {
                                'children': make_diff(node1[key], node2[key]),
                                'type': 'internal_change'}
                                for key in set(node1).intersection(set(node2))
                                if node1[key] != node2[key] and isinstance(
                                node1[key], dict) and isinstance(node2[key],
                                                                 dict)}
    all_dicts = (deleted_items, added_items, unchanged_items,
                 changed_items, changed_items_with_dicts)

    for d in all_dicts:
        diff_dict.update(d)

    return diff_dict


def generate_diff(pathfile1, pathfile2, formater='stylish'):

    format_dict = {'plain': plain, 'json': json_format, 'stylish': stylish}

    ending1, ending2 = pathfile1[-4:], pathfile2[-4:]
    file_data1 = pars(open(pathfile1), ending1)
    file_data2 = pars(open(pathfile2), ending2)

    format_name = format_dict[formater]

    diff_dict = make_diff(file_data1, file_data2)

    return format_name(diff_dict)
