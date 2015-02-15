import collections
import operator
import string
import os


ext_dict = {'clojure': ['.clj', '.clojure'],
            'haskell': ['.hs', '.ghc'],
            'java': ['.java'],
            'javascript': ['.js', '.javascript'],
            'ocaml': ['.ml', '.mli', '.ocaml'],
            'scheme': ['.scm', '.racket', '.ss'],
            'scala': ['.scala'],
            'tcl': ['.tcl'],
            'perl': ['.perl'],
            'php': ['.php'],
            'ruby': ['.rb', '.ruby', '.jruby'],
            'python': ['.python3', '.python2', '.py']
            }


def read_file(code_example):
    """Reads file and returns each line of the file as a list of strings"""
    code = open(code_example, "r")
    try:
        return [line.strip('\n') for line in code.readlines()]
    except UnicodeDecodeError or TypeError:
        print("UnicodeError")


def type_of_file(ext, ext_dict):
    """Determines the type of file based on an extension dictionary"""
    for key, value in ext_dict.items():
        if ext in value:
            return key


def get_file_types(root_directory):
    """Returns the file extensions for each file, as specified by the
    extension dictionary"""
    file_types = []
    for root, directory, files in os.walk(root_directory):
        for code_file in files:
            file_name, extension = os.path.splitext(code_file)
            if extension in [ext for lst in ext_dict.values() for ext in lst]:
                file_types.append(type_of_file(str(extension), ext_dict))
    return file_types


def n_grams(code_file, length):
    """Returns x length punctuation characters from a file. Takes a list of
    strings as input"""
    gram_list = []
    punctuation_list = list(string.punctuation)
    for line in code_file:
        for i in range(len(line) - length):
            gram = line[i:i+length]
            grams = list(gram)
            if set(grams) < set(punctuation_list):
                gram_list.append(gram)
    return gram_list


def top_values(lst, num):
    """Returns top reoccuring values for a list of strings
    lst: list of strings
    num: int, number of top values to return"""
    char_list = []
    value_dict = collections.defaultdict(lambda: 0)
    for value in lst:
        value_dict[value] += 1
    tup_list = sorted(value_dict.items(), key=operator.itemgetter(1),
                      reverse=True)
    for i in range(num):
        try:
            char_list.append(tup_list[i][0])
        except IndexError:
            return char_list
    return char_list


def find_common_characters(language, characters, root_dir):
    """Finds common punctuation characters of a file in a specific language.
    returns a list
    language: string, programming language to search for
    characters: int, length of character strings to return
    root_dir: string, specified directory to search"""
    character_list = []
    for root, directory, files in os.walk(root_dir):
        for code_file in files:
            file_name, extension = os.path.splitext(code_file)
            if extension in [ext for ext in ext_dict[language]]:
                snippet = read_file(root + '/' + code_file)
                character_list.extend(n_grams(snippet, characters))
    return character_list


def check_for_characters(code_file, check_chars):
    """Checks a file for certain character(s) and returns a weighted ratio
    of occurrences/total_characters in file
    -code_file: string, file path
    -check chars: string of list of strings, characters to check
    """

    snippet = read_file(code_file)
    length = len(check_chars)
    total_characters = 0
    count = 0
    for line in snippet:
        for i in range(len(line) - length):
            total_characters += 1
            if line[i:i+length] == check_chars:
                count += 1
    return count/total_characters * 1000  # returning a ratio


def check_character_list(code_file, character_list):
    """Checks a file for each character in the list passed as an argument
    code_file: string, file path"""
    feature_count = []
    for char in character_list:
        count = check_for_characters(code_file, char)
        feature_count.append(count)
    return feature_count


def get_features(char_list, root_dir):
    """Returns the features to use as in a classifier. Returns a 2d array,
    one list per character in char_list.
    char_list: list, list of characters to use as features
    root_dir: string, root directory to search"""
    features = []
    for root, directory, files in os.walk(root_dir):
        for code_file in files:
            if not code_file.startswith('.'):  # to avoid hidden files
                file_name, extension = os.path.splitext(code_file)
                if extension in [ext for lst in ext_dict.values()
                                 for ext in lst]:
                    the_file = root + '/' + code_file
                    count = check_character_list(the_file, char_list)
                    features.append(count)
    return features


def get_test_features(char_list, root_dir):
    """Returns the features to use as in a classifier. Returns a dictionary,
    with the a list of features as a values and the file as a key
    char_list: list, list of characters to use as features
    root_dir: string, root directory to search"""
    features = {}
    for root, directory, files in os.walk(root_dir):
        for code_file in files:
            if not code_file.startswith('.'):  # to avoid hidden files
                the_file = root + '/' + code_file
                count = check_character_list(the_file, char_list)
                features[int(code_file)] = count
    return features
