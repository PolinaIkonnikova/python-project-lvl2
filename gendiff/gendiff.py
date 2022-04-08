import os.path
from .parsing import parsing_data
from .formaters.all_formaters import format_change

ERROR_MESSAGE = "Impossible to build difference. Check your files for validity."


def make_diff(node1, node2):

    def get_difference(key):

        if key in deleted_keys:
            return key, {'type': 'deleted', 'value': node1[key]}

        elif key in added_keys:
            return key, {'type': 'added', 'value': node2[key]}

        elif key in changed_keys and node1[key] == node2[key]:
            return key, {'type': 'unchanged', 'value': node1[key]}

        elif key in changed_keys and node1[key] != node2[key]:
            if isinstance(node1[key], dict) and isinstance(node2[key], dict):
                return key, {'type': 'internal_change',
                             'value': make_diff(node1[key], node2[key])}
            return key, {'type': 'changed_value',
                         'value': [node1[key], node2[key]]}

    all_keys = sorted(set.union(set(node1), set(node2)))
    deleted_keys = set(node1).difference(set(node2))
    added_keys = set(node2).difference(set(node1))
    changed_keys = set(node1).intersection(set(node2))

    return dict(map(get_difference, all_keys))


def get_ending(pathfile):
    return os.path.splitext(pathfile)[1]


def get_data(pathfile):
    with open(pathfile, 'r') as data:
        return parsing_data(data, get_ending(pathfile))


def generate_diff(pathfile1, pathfile2, formater='stylish'):

    data1, data2 = get_data(pathfile1), get_data(pathfile2)

    if (data1 or data2) is False:
        return ERROR_MESSAGE

    diff_dict = make_diff(data1, data2)

    format_style = format_change(formater)

    return format_style(diff_dict)
