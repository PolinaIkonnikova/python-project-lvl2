from . import stylish
from . import plain
from . import json

FORMAT_DICT = {'plain': plain, 'json': json, 'stylish': stylish}


def format_change(format_name):
    return FORMAT_DICT[format_name].make_format
