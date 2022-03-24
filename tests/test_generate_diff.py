import json
from gendiff import generate_diff, get_value


def test_get_value():
    assert get_value('True') == 'true'
    assert isinstance(get_value(56), str)
    dct1 = {1: 2}
    val = get_value(dct1)[1]
    assert isinstance(val, str)


def test_flat_file():
    result1 = open('tests/fixtures/nothing_to_change.txt', 'r').read()
    result2 = open('tests/fixtures/flatfile_stylish.txt', 'r').read()
    assert generate_diff('tests/fixtures/flat1.json',
                         'tests/fixtures/flat1.json') == result1
    assert generate_diff('tests/fixtures/flat1.json',
                         'tests/fixtures/flat2.json') == result2
    assert generate_diff('tests/fixtures/flat1.yaml',
                         'tests/fixtures/flat2.yaml') == result2


def test_gendiff_stylish():
    result3 = open('tests/fixtures/stylish_treefile.txt', 'r').read()
    assert generate_diff('tests/fixtures/tree1.json',
                         'tests/fixtures/tree2.json') == result3
    assert generate_diff('tests/fixtures/tree1.yaml',
                         'tests/fixtures/tree2.yaml') == result3


def test_gendiff_plain():
    result4 = open('tests/fixtures/plain_treefile.txt', 'r').read()
    assert generate_diff('tests/fixtures/tree1.json',
                         'tests/fixtures/tree2.json',
                         'plain') == result4
    assert generate_diff('tests/fixtures/tree1.yaml',
                         'tests/fixtures/tree2.yaml',
                         'plain') == result4
    assert not generate_diff('tests/fixtures/tree1.yaml',
                             'tests/fixtures/tree2.yaml') == result4


def is_json(json_data):
    try:
        json.loads(json_data)
    except ValueError:
        return False
    return True


def test_gendiff_json():
    result1 = generate_diff('tests/fixtures/tree1.json',
                            'tests/fixtures/tree2.json',
                            'json')
    result2 = generate_diff('tests/fixtures/flat1.yaml',
                            'tests/fixtures/flat2.yaml',
                            'json')
    result3 = generate_diff('tests/fixtures/tree1.yaml',
                            'tests/fixtures/tree2.yaml')
    assert is_json(result1) is True
    assert is_json(result2) is True
    assert is_json(result3) is False
