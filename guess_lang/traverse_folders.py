import os
import re
import pandas as pd
from bs4 import BeautifulSoup

""" We want to recognize the following languages:
    Clojure, Haskell, Java, JavaScript,
    OCaml, Perl, PHP, Python,
    Ruby, Scala, Scheme, Tcl """
VALID_EXTENSIONS = ['.clojure', '.hs', '.lhs', '.ghc', '.java',
                    '.javascript', '.js', '.class', '.jar', '.ocaml', '.pl',
                    '.pm', '.t', '.pod', '.perl', '.php',
                    '.phtml', '.php3', '.php4', '.php5', '.phps',
                    '.py', '.pyw', '.pyc', '.pyo', '.pyd',
                    '.python', '.python2', '.python3', '.rb', '.rbw',
                    '.ruby', '.jruby', '.scala', '.scm', '.ss',
                    '.tcl']

LANGUAGE_DICT = {'Clojure': ['.clojure'],
                 'Haskell': ['.hs', '.lhs', '.ghc'],
                 'Java': ['.java', '.class', '.jar'],
                 'JavaScript': ['.js','.javascript'],
                 'OCaml': ['.ocaml'],
                 'Perl': ['.pl', '.pm', '.t', '.pod', '.perl'],
                 'PHP': ['.php', '.phtml', '.php3', '.php4', '.php5', '.phps'],
                 'Python': ['.py', '.pyw', '.pyc', '.pyo', '.pyd',
                            '.python', '.python2','.python3'],
                 'Ruby': ['.rb', '.rbw', '.ruby', '.jruby'],
                 'Scala': ['.scala'],
                 'Scheme': ['.scm', '.ss'],
                 'Tcl': ['.tcl']}

def build_train_set(folder_path):
    """ Builds a list of file paths for files with the acceptable extension. """
    training_code = []
    for directory, subdirs, files in os.walk(folder_path):
        for file in files:
            extension = re.search(r'.(\w+)$',file).group(0)
            if extension and extension in VALID_EXTENSIONS:
                filepath = str(directory) + "/" + str(file)
                """ It doesn't seem like a best possible practice to use a
                dictionary like this but I'm leaning towards brevity and space
                over speed right now. """
                language = "unknown"
                for key, values in LANGUAGE_DICT.items():
                    if extension in values:
                        language = key
                        break
                training_code.append((filepath,language))
    return training_code

def build_test_set(folder_path):
    testing_code = []
    for directory, subdirs, files in os.walk(folder_path):
        for file in files:
            filepath = str(directory) + str(file)
            test_number = int(file)
            testing_code.append((test_number,filepath))
    return testing_code

def get_answers(answer_path):
    df = pd.read_csv(answer_path)
    df.index = df["Filename"]
    return df.to_dict()["Language"]


if __name__ == '__main__':

    files = build_training_set()
    print(files)
