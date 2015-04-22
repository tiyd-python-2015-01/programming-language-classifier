from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
from sklearn.svm import LinearSVC
from programming_language import *
import numpy as np
import pandas as pd
import pickle
import string
import pandas


def get_top_value_lists(language, number_of_values):
    four = find_common_characters(language, 4, 'bench')
    four_list = top_values(four, number_of_values)
    three = find_common_characters(language, 3, 'bench')
    three_list = top_values(three, number_of_values)
    two = find_common_characters(language, 2, 'bench')
    two_list = top_values(two, number_of_values)
    one = find_common_characters(language, 1, 'bench')
    one_list = top_values(one, number_of_values)
    return one_list, two_list, three_list, four_list


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def flip_array(array):
    new_array = np.array(array)
    new_array = new_array.transpose()
    return new_array


number_of_values = 5  # default number of top values for each language
py1, py2, py3, py4 = get_top_value_lists("python", number_of_values)
cloj1, cloj2, cloj3, cloj4 = get_top_value_lists("clojure", number_of_values)
hask1, hask2, hask3, hask4 = get_top_value_lists("haskell", number_of_values)
java1, java2, java3, java4 = get_top_value_lists("java", number_of_values)
js1, js2, js3, js4 = get_top_value_lists("javascript", number_of_values)
oc1, oc2, oc3, oc4 = get_top_value_lists("ocaml", number_of_values)
scm1, scm2, scm3, scm4 = get_top_value_lists("scheme", number_of_values)
scal1, scal2, scal3, scal4 = get_top_value_lists("scala", number_of_values)
perl1, perl2, perl3, perl4 = get_top_value_lists("perl", number_of_values)
php1, php2, php3, php4 = get_top_value_lists("php", number_of_values)
rb1, rb2, rb3, rb4 = get_top_value_lists("ruby", number_of_values)

top_characters_per_language = [py1, py2, py3, py4,
                               cloj1, cloj2, cloj3, cloj4,
                               hask1, hask2, hask3, hask4,
                               java1, java2, java3, java4,
                               js1, js2, js3, js4,
                               oc1, oc2, oc3, oc4,
                               scm1, scm2, scm3, scm4,
                               scal1, scal2, scal3, scal4,
                               perl1, perl2, perl3, perl4,
                               php1, php2, php3, php4,
                               rb1, rb2, rb3, rb4]

top_characters = [char for sublist in top_characters_per_language
                  for char in sublist]

top_chars = remove_duplicates(top_characters)
one_char_punctuation = list(string.punctuation)

strings_and_punctuation = ['"""', '===', '(((', ')))', '/*', '*/', '(*',
                           '*)', '{-', '-}', '#|', '|#', '.(', '--', '::',
                           '//', '))', '{[', '<-', '<=', '=>',
                           '++', '--', '==', 'String', 'string', 'class',
                           'return', 'set', 'argv', 'end', 'expr', 'public',
                           'private', 'function', 'param', 'args', 'format',
                           'module', 'label', 'in', 'len', 'transpose', 'zip',
                           'Length', 'sort_by', 'sorted', 'sort!', 'length',
                           'for', 'enumerate', 'foreach' 'isa', 'is_a', 'ref',
                           'public', '$format', 'else', 'null', 'none', 'proc',
                           'mix', 'defn', 'println', 'ns', 'Integer', 'List',
                           'with', 'Map', 'map', 'Make', 'false', 'False',
                           'True', 'true', 'init', 'search', 'int', 'try',
                           'except', 'if', 'call', 'clojure', 'try', 'except',
                           'list', 'call', 'from', 'let', 'else', 'combine',
                           'self', 'Text', 'where', 'Set', 'include', 'super',
                           'start', 'this', 'dom', 'shutdown', 'system', 'sys',
                           'require', 'extend', 'loc.', 'import', 'get', 'var',
                           'fns', 'replace', 'slice', 'fn', 'exec', 'tuple',
                           'value', 'Array', 'array', 'scala', 'interface',
                           'define', 'port', 'lambda', '|', 'Config',
                           'Module', 'sortBy', 'object', 'val', 'def',
                           'file', 'File', 'val', 'not']

strings_and_punctuation.extend(one_char_punctuation)
top_chars.extend(strings_and_punctuation)
top_punctuation_and_strings = remove_duplicates(top_chars)

#  Getting the test features to analyze for duplicates
test_features = get_test_features(top_punctuation_and_strings, 'test')


def unpack_dict(test_dict):
    test_feat = []
    for k, v in test_dict.items():
        test_feat.append(v)
    return test_feat

test_feat = unpack_dict(test_features)
test_f = flip_array(test_feat)

#  passing the test features into a pandas data frame
test_table = pd.DataFrame(test_f)
test_features_table = test_table.T
test_features_table.columns = top_punctuation_and_strings
test_features_table.head()
# dropping all columns that only have zeros as values
test_table = test_features_table[test_features_table.columns[(test_features_table != 0).any()]]
punctuation_list_scrubbed = list(test_table.columns)
testing = pd.read_csv("test.csv")
testing.head()
test_lang = testing['Language']
train_lang = get_file_types("bench")
train_features = get_features(punctuation_list_scrubbed, 'bench')
test_features = get_test_features(punctuation_list_scrubbed, 'test')
test_feat = []
for k, v in test_features.items():
    test_feat.append(v)

classifier = LinearSVC()
classifier = classifier.fit(train_features, train_lang)
with open('classifier.pickle', 'wb') as pickled_classifier:
    pickle.dump(classifier, pickled_classifier)
