import itertools
import json


REPLACER = ' '
STEP = 2


def output(lines, space):
    return ''.join(itertools.chain(
                   '{\n', lines, space * REPLACER + '}'))


def lines_form(space, status_name, name, value):
    signs_dict = {'deleted': '-', 'added': '+', 'unchanged': ' '}
    sign = signs_dict[status_name]
    return (space + STEP) * REPLACER + f'{sign} {name}: {value}\n'


def make_format(diff_dict):

    def get_value(val, space):

        if isinstance(val, dict):
            result_with_dict = []
            for k, v in val.items():
                line = '{}: {}\n'.format(k, get_value(v, space + 2 * STEP))
                result_with_dict.append((space + 2 * STEP) * REPLACER + line)
            return output(result_with_dict, space)

        if isinstance(val, bool) or val is None:
            return json.dumps(val)

        return str(val)

    def make_lines(item, space):
        name, attributes = item
        status = attributes['type']

        if status == 'internal_change':
            children = attributes['value']
            val = list(map(lambda item: make_lines(item, space + 2 * STEP),
                           children.items()))
            return lines_form(space, 'unchanged', name,
                              output(val, space + 2 * STEP))

        elif status == 'changed_value':
            val_del, val_add = attributes['value']

            first_line = lines_form(space, 'deleted', name,
                                    get_value(val_del, space + 2 * STEP))
            second_line = lines_form(space, 'added', name,
                                     get_value(val_add, space + 2 * STEP))

            return first_line + second_line

        val = attributes['value']
        return lines_form(space, status, name, get_value(val, space + 2 * STEP))

    result = list(map(lambda item: make_lines(item, 0),
                      diff_dict.items()))
    return output(result, 0)
