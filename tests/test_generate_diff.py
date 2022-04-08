import pytest
import json
from gendiff import generate_diff
from gendiff.parsing import parsing_data


@pytest.mark.parametrize('data_file', ['tests/fixtures/flat_files/flat1.json',
                                       'tests/fixtures/flat_files/flat1.yml',
                                       'tests/fixtures/flat_files/flat1.yaml'])
def test_parsing(data_file):
    dict_data = parsing_data(open(data_file), data_file)
    assert isinstance(dict_data, dict)


@pytest.mark.parametrize('data_file', ['tests/fixtures/not_correct/bug.json',
                                       'tests/fixtures/not_correct/empty.yaml',
                                       'tests/fixtures/not_correct/empty.json'])
def test_parsing_not_correct(data_file):
    assert parsing_data(open(data_file), data_file) is False


@pytest.mark.parametrize('data_file1, data_file2, result_file',
                         [('tests/fixtures/flat_files/flat1.json',
                           'tests/fixtures/flat_files/flat1.json',
                           'tests/fixtures/results/nothing_to_change.txt'),
                          ('tests/fixtures/flat_files/flat1.yaml',
                           'tests/fixtures/flat_files/flat2.yaml',
                           'tests/fixtures/results/flatfile_stylish.txt')])
def test_flat_file(data_file1, data_file2, result_file):
    result = open(result_file, 'r').read()
    assert generate_diff(data_file1, data_file2) == result


@pytest.mark.parametrize('data_file1, data_file2, result_file',
                         [('tests/fixtures/tree_files/tree1.json',
                           'tests/fixtures/tree_files/tree2.json',
                           'tests/fixtures/results/stylish_treefile.txt'),
                          ('tests/fixtures/tree_files/tree1.yaml',
                           'tests/fixtures/tree_files/tree2.yaml',
                           'tests/fixtures/results/stylish_treefile.txt')])
def test_gendiff_stylish(data_file1, data_file2, result_file):
    result = open(result_file, 'r').read()
    assert generate_diff(data_file1, data_file2) == result


@pytest.mark.parametrize('data_file1, data_file2, result_file',
                         [('tests/fixtures/tree_files/tree1.json',
                           'tests/fixtures/tree_files/tree2.json',
                           'tests/fixtures/results/plain_treefile.txt'),
                          ('tests/fixtures/tree_files/tree1.json',
                           'tests/fixtures/tree_files/tree1.json',
                           'tests/fixtures/results/empty_res_plain.txt')])
def test_gendiff_plain(data_file1, data_file2, result_file):
    result = open(result_file, 'r').read()
    assert generate_diff(data_file1, data_file2, 'plain') == result
    assert not generate_diff(data_file1, data_file2) == result


def is_json(json_data):
    try:
        json.loads(json_data)
    except ValueError:
        return False
    return True


@pytest.mark.parametrize('data_file1, data_file2',
                         [('tests/fixtures/tree_files/tree1.yaml',
                           'tests/fixtures/tree_files/tree2.json'),
                          ('tests/fixtures/tree_files/tree1.json',
                           'tests/fixtures/tree_files/tree1.json')])
def test_gendiff_json(data_file1, data_file2):
    result1 = generate_diff(data_file1, data_file2, 'json')
    result2 = generate_diff(data_file1, data_file2)
    assert is_json(result1) is True
    assert is_json(result2) is False
