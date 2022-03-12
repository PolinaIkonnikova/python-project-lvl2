import itertools


def flatten(node_list):
    result = []

    def walk(lst):
        for item in lst:
            if isinstance(item, list):
                walk(item)
            else:
                result.append(item)
    walk(node_list)
    return result


def get_value(val):
    bool_list = {'true', 'false', 'null'}
    if isinstance(val, dict):
        return '[complex value]'
    if val in bool_list:
        return val
    return "'{}'".format(val)


def plain(node_list):
    path = []

    def make_lines(node_list, path):
        result = []
        node_list = sorted(node_list, key=lambda x: x['name'])
        for node in list(filter(lambda x: x['status'] != "unchanged",
                                node_list)):
            path_record = list(itertools.chain(path, [str(node['name'])]))
            if node['status'] == 'internal_change':
                line = make_lines(node['value'], path_record)

            elif node['status'] == 'added':
                line = "Property '{}' was added with value: {}".format(
                    '.'.join(path_record), get_value(node['value']))

            elif node['status'] == 'deleted':
                line = "Property '{}' was removed".format('.'.join(path_record))

            elif node['status'] == 'changed_value':
                line = "Property '{}' was updated. From {} to {}".format(
                    '.'.join(path_record), get_value(node['value'][0]),
                    get_value(node['value'][1]))
            result.append(line)
        return result
    output = make_lines(node_list, path)
    return '\n'.join(flatten(output))
