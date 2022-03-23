import itertools


REPLACER = ' '
STEP = 2


def output(lines, space):
    return ''.join(itertools.chain(
                   '{\n', lines, space * REPLACER + '}'))


def sorted_dict(dct):
    return dict(sorted(dct.items(), key=lambda x: x[0]))


def stylish(diff_dict):
    signs_dict = {'deleted': '-', 'added': '+', 'unchanged': ' '}

    def get_value(val, space):
        if isinstance(val, dict):
            result_with_dict = []
            for k, v in val.items():
                line = '{}: {}\n'.format(k, get_value(v, space + 2 * STEP))
                result_with_dict.append((space + 2 * STEP) * REPLACER + line)
            return output(sorted(result_with_dict), space)
        return val

    def make_lines(item, space):
        output_line = (space + STEP) * REPLACER + '{} {}: {}\n'
        name, attributes = item
        status = attributes['type']

        if status == 'internal_change':
            children = attributes['children']
            val = list(map(lambda item: make_lines(item, space + 2 * STEP),
                           sorted_dict(children).items()))
            return output_line.format(signs_dict['unchanged'],
                                      name, output(val, space + 2 * STEP))

        if status == 'changed_value':
            val_del = attributes['value'][0]
            val_add = attributes['value'][1]
            first_line = output_line.format(signs_dict['deleted'], name,
                                            get_value(val_del,
                                            space + 2 * STEP))
            second_line = output_line.format(signs_dict['added'], name,
                                             get_value(val_add,
                                             space + 2 * STEP))
            return first_line + second_line

        val = attributes['value']
        return output_line.format(signs_dict[status], name,
                                  get_value(val, space + 2 * STEP))

    result = list(map(lambda item: make_lines(item, 0),
                      sorted_dict(diff_dict).items()))
    return output(result, 0)
