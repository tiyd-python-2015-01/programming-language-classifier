import os
import re

""" We want to recognize the following languages:
    Clojure, Haskell, Java, JavaScript,
    OCaml, Perl, PHP, Python,
    Ruby, Scala, Scheme, Tcl """
VALID_EXTENSIONS = ['.clojure', '.hs', '.lhs', '.java', '.class', '.jar',
                    '.ghc', '.ocaml', '.pl', '.pm', '.t', '.pod', '.perl',
                    '.php', '.phtml', 'php3', '.php4', 'php5', 'phps',
                    '.py', '.pyw', '.pyc', '.pyo', '.pyd', '.python', 'python2', 'python3',
                    '.rb', '.rbw', '.ruby', '.jruby', '.scala',
                    '.scm', '.ss', '.tcl']

LANGUAGE_DICT = {'Clojure': ['.clojure'],
                 'Haskell': ['.hs', '.lhs', '.ghc'],
                 'Java': ['.java', '.class', '.jar'],
                 'JavaScript': ['.js'],
                 'OCaml': ['.ocaml'],
                 'Perl': ['.pl', '.pm', '.t', '.pod', '.perl'],
                 'PHP': ['.php', '.phtml', 'php3', '.php4', 'php5', 'phps'],
                 'Python': ['.py', '.pyw', '.pyc', '.pyo', '.pyd',
                            '.python', 'python2','python3'],
                 'Ruby': ['.rb', '.rbw', '.ruby', '.jruby'],
                 'Scala': ['.scala'],
                 'Scheme': ['.scm', '.ss'],
                 'Tcl': ['.tcl']}

def build_training_set():
    """ Builds a list of file paths for files with the acceptable extension. """
    training_code = []
    n = 0
    for directory, subdirs, files in os.walk("guess_lang/data/"):
        for file in files:

            extension = re.search(r'.(\w+)$',file)
            if extension and extension.group(0) in VALID_EXTENSIONS:
                filepath = str(directory) + "/" + str(file)
                training_code.append(filepath)
    return training_code

if __name__ == '__main__':

    files = build_training_set()
    print(files)
