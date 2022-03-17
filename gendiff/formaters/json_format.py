import json


def json_format(node_list):
    json_dict = {}

    def make_json(node):
        if node['status'] == 'internal_change':
            return {node['name']: list(map(make_json, node['children']))}
        if node['status'] == 'changed_value':
            return {node['name']: (('deleted', node['value'][0]),
                                   ('added', node['value'][1]))}
        return {node['name']: (node['status'], node['value'])}

    output = list(map(make_json, node_list))

    for item in output:
        json_dict.update(item)

    return json.dumps(json_dict, indent=3, sort_keys=True)
