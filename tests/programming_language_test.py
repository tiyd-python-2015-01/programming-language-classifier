import programming_language as pl
from programming_language import ext_dict

file = pl.read_file('test/1')
gram_list = pl.n_grams(file, 1)

def test_read_file():
    assert len(file) == 30  # 'test/1' is 30 lines long

def test_type_of_file():
    ext = pl.type_of_file('.py', ext_dict)
    assert ext == 'python'

def test_get_file_types():
    types = pl.get_file_types('bench')
    assert 'clojure' in types

def test_n_grams():
    assert len(gram_list[0]) == 1

def test_top_values():
    values = pl.top_values(gram_list, 5)
    assert len(values) == 5

def test_find_common_characters():
    chars = pl.find_common_characters('python', 2, 'bench')
    assert len(chars[0]) == 2

def test_check_character_list():
    char_list = pl.check_character_list('test/1', [')', '('])
    assert len(char_list) == 2
    assert char_list[0] > 0

def test_get_features():
    features = pl.get_features([')', '('], 'bench')
    assert len(features) > 0

def test_get_test_features():
    features = pl.get_test_features([')', '('], 'test')
    assert len(features.items()) > 0
