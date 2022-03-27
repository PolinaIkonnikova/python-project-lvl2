import itertools
import json

def get_value(val):

    if isinstance(val, dict):
        return '[complex value]'

    if isinstance(val, bool) or val is None:
            return json.dumps(val)

    if isinstance(val, int) or isinstance(val, float) :
        return str(val)

    return "'{}'".format(str(val))


def get_dict(dct):
    return dict(filter(lambda item: item[1]['type'] != 'unchanged',
                       dct.items()))

def plain(diff_dict):
    path = []

    def make_plain(item, path):
        name, attributes = item
        status = attributes['type']
        path_record = list(itertools.chain(path, [str(name)]))

        if status == 'internal_change':
            children = attributes['value']
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

    return '\n'.join(list(map(lambda item: make_plain(item, path),
                                get_dict(diff_dict).items())))
