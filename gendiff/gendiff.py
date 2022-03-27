import os.path
from .parsing import pars
from .formaters.stylish import stylish
from .formaters.plain import plain
from .formaters.json_format import json_format


def make_shape(key, val, type_name):
    return {key: {'type': type_name, 'value': val}}


def make_diff(node1, node2):

    diff_dict = {}

    deleted_keys = set(node1).difference(set(node2))
    added_keys = set(node2).difference(set(node1))
    other_keys = set(node1).intersection(set(node2))

    for key in deleted_keys:
        diff_dict.update(make_shape(key, node1[key], 'deleted'))

    for key in added_keys:
        diff_dict.update(make_shape(key, node2[key], 'added'))

    for key in other_keys:
        if node1[key] == node2[key]:
            diff_dict.update(make_shape(key, node1[key],
                                        'unchanged'))
        else:
            if isinstance(node1[key], dict) and isinstance(node2[key], dict):
                diff_dict.update(make_shape(key, make_diff(node1[key],
                                            node2[key]), 'internal_change'))

            else:
                diff_dict.update(make_shape(key, [node1[key], node2[key]],
                                            'changed_value'))

    return dict(sorted(diff_dict.items(), key=lambda x: x[0]))


def generate_diff(pathfile1, pathfile2, formater='stylish'):

    format_dict = {'plain': plain, 'json': json_format, 'stylish': stylish}

    file_data1 = pars(open(pathfile1), os.path.splitext(pathfile1)[1])
    file_data2 = pars(open(pathfile2), os.path.splitext(pathfile2)[1])

    format_name = format_dict[formater]

    diff_dict = make_diff(file_data1, file_data2)

    return format_name(diff_dict)
