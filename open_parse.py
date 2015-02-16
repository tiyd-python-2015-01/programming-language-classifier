import os
import re
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn import metrics


def open_read_file(file):
    """Opens a file and returns it as a string of text."""
    with open(file) as text:
        clean = re.sub('[\t]', '    ', text.read())
        clean = re.sub('[\n]', '', clean)
    return clean


def get_filepaths(directory):
    """Obtains the desired file paths for files in a directory and its subs."""
    extensions = (".clj", ".cljs", ".edn", ".clojure",
                  ".hs", ".lhs", ".ghc",".java", ".jar",
                  ".js", ".javascript", ".ml", ".pl",
                  ".pm", ".t", ".pod", ".php", ".phtml", ".ocaml",
                  ".php4", ".php3", ".php5", ".phps", ".perl",
                  ".py", ".pyw", ".pyc", ".pyo", ".pyd",
                  ".python3", "rb", ".rbw", '.ruby', ".jruby", ".scala",
                  ".scm", ".ss", ".racket", ".tcl", ".racket")
    file_paths = []
    for root, subdir, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extensions):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
    return file_paths


def get_lang(ext):
    """Returns the name of the language of a file based on the extension."""
    if ext in ['.clj', '.cljs', '.edn', '.clojure']:
        return 'Clojure'
    elif ext in ['.hs', '.lhs', '.ghc']:
        return 'Haskell'
    elif ext in ['.java', '.jar']:
        return 'Java'
    elif ext in ['.js', '.javascript']:
        return 'Javascript'
    elif ext in ['.ml', '.ocaml']:
        return 'OCaml'
    elif ext in ['.pl', '.pm', '.t', '.pod', '.perl']:
        return 'Perl'
    elif ext in ['.php', '.phtml', '.php4', '.php3', '.php5', '.phps']:
        return 'PHP'
    elif ext in ['.py', '.pyw', '.pyc', '.pyo', '.pyd', '.python3']:
        return 'Python'
    elif ext in ['.rb', '.rbw', '.ruby', '.jruby']:
        return 'Ruby'
    elif ext == '.scala':
        return 'Scala'
    elif ext in ['.scm', '.ss', '.racket']:
        return 'Scheme'


def slash_star(snippets):
    count = 0
    count = len(list(re.finditer(r"/\*", snippets)))
    return count


def two_semicolons(snippets):
    count = 0
    count = len(list(re.finditer(r";{2}", snippets)))
    return count


def print_statement(snippets):
    count = 0
    count = len(list(re.finditer(r".print.", snippets)))
    return count


def puts(snippets):
    count = 0
    count = len(list(re.finditer(r".puts.", snippets)))
    return count


def val(snippets):
    count = 0
    count = len(list(re.finditer(r".val.", snippets)))
    return count


def money(snippets):
    count = 0
    count = len(list(re.finditer(r".\$.", snippets)))
    return count


def caml_star(snippets):
    count = 0
    count = len(list(re.finditer(r"\(\*" , snippets)))
    return count


def star_c(snippets):
    count = 0
    count = len(list(re.finditer(r"\*\)" , snippets)))
    return count


def public(snippets):
    count = 0
    count = len(list(re.finditer(r".public.", snippets)))
    return count


def static(snippets):
    count = 0
    count = len(list(re.finditer(r".static.", snippets)))
    return count


def void(snippets):
    count = 0
    count = len(list(re.finditer(r".void.", snippets)))
    return count


def var(snippets):
    count = 0
    count = len(list(re.finditer(r".var.", snippets)))
    return count


def let(snippets):
    count = 0
    count = len(list(re.finditer(r".let.", snippets)))
    return count


def require(snippets):
    count = 0
    count = len(list(re.finditer(r".require.", snippets)))
    return count


def end(snippets):
    count = 0
    count = len(list(re.finditer(r".end.", snippets)))
    return count


def private(snippets):
    count = 0
    count = len(list(re.finditer(r".private.", snippets)))
    return count


def double_colon(snippets):
    count = 0
    count = len(list(re.finditer(r".::.", snippets)))
    return count


def read_json(snippets):
    count = 0
    count = len(list(re.finditer(r".readJSON.", snippets)))
    return count


def arrow(snippets):
    count = 0
    count = len(list(re.finditer(r".->.", snippets)))
    return count


def curly_dash(snippets):
    count = 0
    count = len(list(re.finditer(r".{-.", snippets)))
    return count


def defn(snippets):
    count = 0
    count = len(list(re.finditer(r".defn.", snippets)))
    return count


def pipe(snippets):
    count = 0
    count = len(list(re.finditer(r" | ", snippets)))
    return count


def double_slash(snippets):
    count = 0
    count = len(list(re.finditer(r".// .", snippets)))
    return count


def object_str(snippets):
    count = 0
    count = len(list(re.finditer(r".object.", snippets)))
    return count


def elif_str(snippets):
    count = 0
    count = len(list(re.finditer(r".elif.", snippets)))
    return count


def else_str(snippets):
    count = 0
    count = len(list(re.finditer(r"else:", snippets)))
    return count


def implicit(snippets):
    count = 0
    count = len(list(re.finditer(r".implicit.", snippets)))
    return count


def extends(snippets):
    count = 0
    count = len(list(re.finditer(r".extends.", snippets)))
    return count


def triple_quotes(snippets):
    count = 0
    count = len(list(re.finditer(r'.""".', snippets)))
    return count


def import_str(snippets):
    count = 0
    count = len(list(re.finditer(r'.import.', snippets)))
    return count


def dollar_format(snippets):
    count = 0
    count = len(list(re.finditer(r'.\$format.', snippets)))
    return count


def return_str(snippets):
    count = 0
    count = len(list(re.finditer(r'.return.', snippets)))
    return count


def dollar_container(snippets):
    count = 0
    count = len(list(re.finditer(r'.\$container.', snippets)))
    return count


def semi_space(snippets):
    count = 0
    count = len(list(re.finditer(r'.; .', snippets)))
    return count


def dunder_init(snippets):
    count = 0
    count = len(list(re.finditer(r'.__init__.', snippets)))
    return count


def parens_define(snippets):
    count = 0
    count = len(list(re.finditer(r'.\(define.', snippets)))
    return count


def parens_semi(snippets):
    count = 0
    count = len(list(re.finditer(r'.\);.', snippets)))
    return count


def class_str(snippets):
    count = 0
    count = len(list(re.finditer(r'.class.', snippets)))
    return count


def do(snippets):
    count = 0
    count = len(list(re.finditer(r'.do.', snippets)))
    return count


def parens_true(snippets):
    count = 0
    count = len(list(re.finditer(r'.\(true\).', snippets)))
    return count


def open_and_parse(path):
    """Takes a directory path and returns a dataframe of all the desired files
       with their corresponding feature scores."""
    file_paths = get_filepaths(path)
    df = []
    for paths in file_paths:
       df.append(open_read_file(paths))
    df = np.array(df)
    df = pd.DataFrame(df)
    df = df.rename(columns={0: 'Snippet'})
    df[';;'] = df['Snippet'].apply(two_semicolons)
    df['/*'] = df['Snippet'].apply(slash_star)
    #df['print'] = df['Snippet'].apply(print_statement)
    df['val'] = df['Snippet'].apply(val)
    df['$'] = df['Snippet'].apply(money)
    df['(*'] = df['Snippet'].apply(caml_star)
    df['*)'] = df['Snippet'].apply(star_c)
    df['static'] = df['Snippet'].apply(static)
    df['var'] = df['Snippet'].apply(var)
    df['let'] = df['Snippet'].apply(let)
    df['end'] = df['Snippet'].apply(end)
    df['::'] = df['Snippet'].apply(double_colon)
    df['defn'] = df['Snippet'].apply(defn)
    df['|'] = df['Snippet'].apply(pipe)
    df['//'] = df['Snippet'].apply(double_slash)
    df['object'] = df['Snippet'].apply(object_str)
    df['elif'] = df['Snippet'].apply(elif_str)
    df['else'] = df['Snippet'].apply(else_str)
    df['import'] = df['Snippet'].apply(import_str)
    df['$format'] = df['Snippet'].apply(dollar_format)
    df['return'] = df['Snippet'].apply(return_str)
    df['$container'] = df['Snippet'].apply(dollar_container)
    #df['; '] = df['Snippet'].apply(semi_space)
    df['__init__'] = df['Snippet'].apply(dunder_init)
    df['(define'] = df['Snippet'].apply(parens_define)
    df[');'] = df['Snippet'].apply(parens_semi)
    df['class'] = df['Snippet'].apply(class_str)
    df['do'] = df['Snippet'].apply(do)
    df['(true)'] = df['Snippet'].apply(parens_true)
    return df


def open_and_parse_single(path):
    """Takes a file path and returns a dataframe with the file's
       corresponding feature scores."""
    df = []
    df.append(open_read_file(path))
    df = np.array(df)
    df = pd.DataFrame(df)
    df = df.rename(columns={0: 'Snippet'})
    df[';;'] = df['Snippet'].apply(two_semicolons)
    df['/*'] = df['Snippet'].apply(slash_star)
    #df['print'] = df['Snippet'].apply(print_statement)
    df['val'] = df['Snippet'].apply(val)
    df['$'] = df['Snippet'].apply(money)
    df['(*'] = df['Snippet'].apply(caml_star)
    df['*)'] = df['Snippet'].apply(star_c)
    df['static'] = df['Snippet'].apply(static)
    df['var'] = df['Snippet'].apply(var)
    df['let'] = df['Snippet'].apply(let)
    df['end'] = df['Snippet'].apply(end)
    df['::'] = df['Snippet'].apply(double_colon)
    df['defn'] = df['Snippet'].apply(defn)
    df['|'] = df['Snippet'].apply(pipe)
    df['//'] = df['Snippet'].apply(double_slash)
    df['object'] = df['Snippet'].apply(object_str)
    df['elif'] = df['Snippet'].apply(elif_str)
    df['else'] = df['Snippet'].apply(else_str)
    df['import'] = df['Snippet'].apply(import_str)
    df['$format'] = df['Snippet'].apply(dollar_format)
    df['return'] = df['Snippet'].apply(return_str)
    df['$container'] = df['Snippet'].apply(dollar_container)
    #df['; '] = df['Snippet'].apply(semi_space)
    df['__init__'] = df['Snippet'].apply(dunder_init)
    df['(define'] = df['Snippet'].apply(parens_define)
    df[');'] = df['Snippet'].apply(parens_semi)
    df['class'] = df['Snippet'].apply(class_str)
    df['do'] = df['Snippet'].apply(do)
    df['(true)'] = df['Snippet'].apply(parens_true)
    return df
