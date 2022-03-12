import itertools


REPLACER = ' '


def output(lines, space):
    return ''.join(itertools.chain(
                   '{\n', lines, space * REPLACER + '}'))


def stylish(node_list):
    signs_dict = {'deleted': '-', 'added': '+', 'unchanged': ' '}
    step = 2
    node_list = sorted(node_list, key=lambda node: node['name'])

    def get_value(val, space):
        if isinstance(val, dict):
            result_with_dict = []
            for k, v in val.items():
                line = (space + 2 * step)*REPLACER + '{}: {}\n'.format(k,
                                        get_value(v, space + 2 * step))
                result_with_dict.append(line)
            return output(sorted(result_with_dict), space)
        return val

    def make_lines(node_list, space):

        output_line = (space + step) * REPLACER + '{} {}: {}\n'

        node_list = sorted(node_list, key=lambda node: node['name'])

        result = []
        for node in node_list:
            if node['status'] == 'internal_change':
                val = make_lines(node['value'], space + 2 * step)
                new_line = output_line.format(
                            signs_dict['unchanged'],
                             node['name'], val)
            elif node['status'] == 'changed_value':
                val_del = node['value'][0]
                val_add = node['value'][1]
                first_line = output_line.format(
                                       signs_dict['deleted'], node['name'],
                                       get_value(val_del, space + 2 * step))
                second_line = output_line.format(
                            signs_dict['added'], node['name'],
                              get_value(val_add, space + 2 * step))
                new_line = first_line + second_line
            else:
                new_line = output_line.format(
                            signs_dict[node['status']], node['name'],
                             get_value(node['value'], space + 2 * step))
            result.append(new_line)
        return output(result, space)
    return make_lines(node_list, 0)
