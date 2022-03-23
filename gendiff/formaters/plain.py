import itertools


def get_value(val):
    json_format_set = {'true', 'false', 'null'}
    if isinstance(val, dict):
        return '[complex value]'
    if val in json_format_set:
        return val
    if val.isdigit():
        return val
    return "'{}'".format(val)


def get_dict(dct):
    return dict(filter(lambda item: item[1]['type'] != 'unchanged',
                       sorted(dct.items(), key=lambda x: x[0])))


def plain(node_list):
    path = []

    def make_plain(item, path):
        name, attributes = item
        status = attributes['type']
        path_record = list(itertools.chain(path, [str(name)]))

        if status == 'internal_change':
            children = attributes['children']
            return '\n'.join(list(map(
                             lambda item: make_plain(item, path_record),
                             get_dict(children).items())))

        elif status == 'added':
            val = attributes['value']
            return "Property '{}' was added with value: {}".format(
                '.'.join(path_record), get_value(val))

        elif status == 'deleted':
            return "Property '{}' was removed".format('.'.join(path_record))

        elif status == 'changed_value':
            del_val = attributes['value'][0]
            add_val = attributes['value'][1]
            return "Property '{}' was updated. From {} to {}".format(
                '.'.join(path_record), get_value(del_val),
                get_value(add_val))
        elif status == 'unchanged':
            return ''

    output = '\n'.join(list(map(lambda item: make_plain(item, path),
                                get_dict(node_list).items())))

    return output
