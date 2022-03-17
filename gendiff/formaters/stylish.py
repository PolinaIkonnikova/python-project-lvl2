import itertools


REPLACER = ' '
STEP = 2


def output(lines, space):
    return ''.join(itertools.chain(
                   '{\n', lines, space * REPLACER + '}'))


def get_value(val, space):
    if isinstance(val, dict):
        result_with_dict = []
        for k, v in val.items():
            line = '{}: {}\n'.format(k, get_value(v, space + 2 * STEP))
            result_with_dict.append((space + 2 * STEP) * REPLACER + line)
        return output(sorted(result_with_dict), space)
    return val


def stylish(node_list):
    signs_dict = {'deleted': '-', 'added': '+', 'unchanged': ' '}

    def make_lines(node, space):
        output_line = (space + STEP) * REPLACER + '{} {}: {}\n'

        if node['status'] == 'internal_change':
            val = make_stylish(node['children'], space + 2 * STEP)
            new_line = output_line.format(signs_dict['unchanged'],
                                          node['name'], val)
            return new_line

        elif node['status'] == 'changed_value':
            val_del = node['value'][0]
            val_add = node['value'][1]
            first_line = output_line.format(signs_dict['deleted'],
                                            node['name'],
                                            get_value(val_del,
                                            space + 2 * STEP))
            second_line = output_line.format(signs_dict['added'],
                                             node['name'],
                                             get_value(val_add,
                                             space + 2 * STEP))
            return first_line + second_line

        new_line = output_line.format(signs_dict[node['status']],
                                      node['name'],
                                      get_value(node['value'],
                                      space + 2 * STEP))
        return new_line

    def make_stylish(node_list, space):
        node_list = sorted(node_list, key=lambda node: node['name'])
        result = list(map(lambda node: make_lines(node, space), node_list))
        return output(result, space)

    return make_stylish(node_list, 0)
