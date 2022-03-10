import itertools


#a = [{'status': 'deleted', 'name': 'group3', 'value': {'fee': 100500, 'deep': {'id': {'number': 45}}}}, {'status': 'added', 'name': 'group2', 'value': {'abc': 12345, 'deep': {'id': 45}}}, {'status': 'internal_change', 'name': 'group1', 'value': [{'status': 'unchanged', 'name': 'foo', 'value': 'bar'}, {'status': 'changed_value', 'name': 'nest', 'value': ['str', {'key': 'value'}]}, {'status': 'changed_value', 'name': 'baz', 'value': ['bars', 'bas']}]}, {'status': 'internal_change', 'name': 'common', 'value': [{'status': 'deleted', 'name': 'setting4', 'value': 'blah blah'}, {'status': 'deleted', 'name': 'setting5', 'value': {'key5': 'value5'}}, {'status': 'deleted', 'name': 'follow', 'value': 'false'}, {'status': 'added', 'name': 'setting2', 'value': 200}, {'status': 'unchanged', 'name': 'setting1', 'value': 'Value 1'}, {'status': 'changed_value', 'name': 'setting3', 'value': [None, True]}, {'status': 'internal_change', 'name': 'setting6', 'value': [{'status': 'deleted', 'name': 'ops', 'value': 'vops'}, {'status': 'unchanged', 'name': 'key', 'value': 'value'}, {'status': 'internal_change', 'name': 'doge', 'value': [{'status': 'changed_value', 'name': 'wow', 'value': ['so much', '']}]}]}]}]

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
                line = "Property '{}' was added with value: {}".format('.'.join(path_record),
                                                        get_value(node['value']))

            elif node['status'] == 'deleted':
                line = "Property '{}' was removed".format('.'.join(path_record))

            elif node['status'] == 'changed_value':
                line = "Property '{}' was updated. From {} to {}".format('.'.join(path_record),
                      get_value(node['value'][0]),
                      get_value(node['value'][1]))
            result.append(line)
        return result
    output = make_lines(node_list, path)
    return '\n'.join(flatten(output))


