import itertools
from gendiff.misc.flatten import flatten


def get_value(val):
    json_format_set = {'true', 'false', 'null'}
    if isinstance(val, dict):
        return '[complex value]'
    if val in json_format_set:
        return val
    if val.isdigit():
        return val
    return "'{}'".format(val)


def plain(node_list):
    path = []

    def make_plain(node_list, path):
        node_list = list(filter(lambda x: x['status'] != "unchanged",
                         sorted(node_list, key=lambda x: x['name'])))
        return list(map(lambda node: make_lines(node, path), node_list))

    def make_lines(node, path):

        path_record = list(itertools.chain(path, [str(node['name'])]))

        if node['status'] == 'internal_change':
            return make_plain(node['children'], path_record)

        elif node['status'] == 'added':
            return "Property '{}' was added with value: {}".format(
                '.'.join(path_record), get_value(node['value']))

        elif node['status'] == 'deleted':
            return "Property '{}' was removed".format('.'.join(path_record))

        elif node['status'] == 'changed_value':
            return "Property '{}' was updated. From {} to {}".format(
                '.'.join(path_record), get_value(node['value'][0]),
                get_value(node['value'][1]))

    output = make_plain(node_list, path)

    return '\n'.join(flatten(output))
