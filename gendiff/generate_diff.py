import itertools, json
import  yaml
from .formaters import stylish, plain, json_format


def pars(pathfile):
    if pathfile.endswith('.yaml') or pathfile.endswith('.yml'):
        with open(pathfile) as f:
            read_data = yaml.load(f, Loader=yaml.FullLoader)
        return read_data
    elif pathfile.endswith('.json'):
        return json.load(open(pathfile))
    return


def flatten(result_list):
    result = []
    def walk(lst):
        for item in lst:
            if isinstance(item, list):
                walk(item)
            else:
                result.append(item)
    walk(result_list)
    return result


def generate_diff(pathfile1, pathfile2, formater='stylish'):

    format_dict = {'plain': plain, 'json': json_format, 'stylish': stylish}

    file_data1 = pars(pathfile1)
    file_data2 = pars(pathfile2)

    def diff_record(node1, node2):

        def get_value(val):

            js_values = {True: 'true', False: 'false', None: 'null'}

            if isinstance(val, dict):
                return {k: get_value(v) for k, v in val.items()}

            if val in js_values:
                return js_values[val]
            return val

        deleted_keys = set(node1).difference(set(node2))

        added_keys = set(node2).difference(set(node1))

        unchanged_keys = {key for key in set(node1).intersection(set(node2))
                          if node1[key] == node2[key]}

        changed_keys = {key for key in set(node1).intersection(set(node2))
                        if node1[key] != node2[key] and
                        (not(isinstance(node1[key], dict)) or
                        not(isinstance(node2[key], dict)))}

        changed_keys_with_dicts = {key for key in
                                   set(node1).intersection(set(node2))
                                   if node1[key] != node2[key] and
                                   isinstance(node1[key], dict) and
                                   isinstance(node2[key], dict)}


        def make_diff(node, key_set, status):
            internal_repr = []
            for key in key_set:
                if key_set == changed_keys_with_dicts:
                    representation = dict([('name', key),
                                           ('value',
                                             diff_record(node1[key], node2[key])),
                                           ('status', status)])
                elif key_set == changed_keys:
                    representation = dict([('name', key),
                                            ('value', [node1[key], node2[key]]),
                                            ('status', status)])
                else:
                    representation = dict([('name', key),
                                           ('value', get_value(node[key])),
                                           ('status', status)])

                internal_repr.append(representation)
            return internal_repr

        result = list(filter(lambda x: len(x) > 0, itertools.starmap(make_diff, [
                             (node1, deleted_keys, 'deleted'),
                             (node2, added_keys, 'added'),
                             (node1, unchanged_keys, 'unchanged'),
                             (node1, changed_keys, 'changed_value'),
                             (node1, changed_keys_with_dicts, 'internal_change')
                              ])))
        return flatten(result)

    diff_list = diff_record(file_data1, file_data2)
    return format_dict[formater](diff_list)