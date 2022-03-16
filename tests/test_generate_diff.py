import json
from gendiff import generate_diff


result1 = open('tests/fixtures/result1_nothing_to_change.txt', 'r').read()
result2 = open('tests/fixtures/result2_flatfile.txt', 'r').read()
result3 = open('tests/fixtures/result3_stylish_treefile.txt', 'r').read()
result4 = open('tests/fixtures/result4_plain_treefile.txt', 'r').read()
result5 = open('tests/fixtures/result5_json_treefile.txt', 'r').read()


def test_flat_file():
    result1 = open('tests/fixtures/result1_nothing_to_change.txt', 'r').read()
    result2 = open('tests/fixtures/result2_flatfile.txt', 'r').read()
    assert generate_diff('tests/fixtures/file1.json',
                         'tests/fixtures/file1.json') == result1
    assert generate_diff('tests/fixtures/file1.json',
                         'tests/fixtures/file2.json') == result2
    assert generate_diff('tests/fixtures/file1.yaml',
                         'tests/fixtures/file2.yaml') == result2


def test_gendiff_stylish():
    assert generate_diff('tests/fixtures/dict1.json',
                         'tests/fixtures/dict2.json') == result3
    assert generate_diff('tests/fixtures/dict1.yaml',
                         'tests/fixtures/dict2.yaml') == result3


def test_gendiff_plain():
    assert generate_diff('tests/fixtures/dict1.json',
                         'tests/fixtures/dict2.json',
                         'plain') == result4
    assert generate_diff('tests/fixtures/dict1.yaml',
                         'tests/fixtures/dict2.yaml',
                         'plain') == result4
    assert not generate_diff('tests/fixtures/dict1.yaml',
                             'tests/fixtures/dict2.yaml') == result4


def is_json(json_data):
    try:
        json_object = json.loads(json_data)
    except ValueError:
        return False
    return True


def test_gendiff_json():
    json_data_1 = generate_diff('tests/fixtures/dict1.json',
                                'tests/fixtures/dict2.json',
                                'json')
    json_data_2 = generate_diff('tests/fixtures/file1.yaml',
                                'tests/fixtures/file2.yaml',
                                'json')
    json_data_3 = generate_diff('tests/fixtures/dict1.yaml',
                                'tests/fixtures/dict2.yaml')
    assert is_json(json_data_1) is True
    assert is_json(json_data_2) is True
    assert is_json(json_data_3) is False
