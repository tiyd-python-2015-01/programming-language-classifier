import pandas as pd
import numpy as np
import os
from textblob import TextBlob


prog_langs = {"clojure": [".clj", ".cljs", ".edn", ".clojure"],
             "haskell" : [".hs", ".lhs", ".ghc"],
             "java": [".java", ".jar", ".class"],
             "javascript": [".js", ".javascript"],
             "ocaml": [".ml", ".ocaml"],
             "perl" : [".pl", ".pm", ".t", ".pod", ".perl"],
             "php" : [".php", ".phtml", ".php4", ".php3", ".php5", ".phps"],
             "python" : [".py", ".pyw", ".pyc", ".pyo", ".pyd", ".python3"],
             "ruby" : ["rb", ".rbw", ".jruby"],
             "scala" : [".scala"],
             "scheme" : [".scm", ".ss", ".racket"]
             }


extensions = (".clj", ".cljs", ".edn", ".clojure",
             ".hs", ".lhs", ".ghc",".java", ".jar",
             ".js", ".javascript", ".ml", ".pl",
             ".pm", ".t", ".pod", ".php", ".phtml",
             ".php4", ".php3", ".php5", ".phps",
             ".py", ".pyw", ".pyc", ".pyo", ".pyd",
             ".python3", "rb", ".rbw", ".scala",
             ".scm", ".ss", ".racket", ".perl", ".ocaml",
             ".jruby")


def get_corpus(dir_path):
    """Goes into a directory and all the directories below it. In each
    directory it find all files of a certain type, and adds their text to
    a list. Once it has searched through each directory it creates a dataframe
    with all of the text from each file and what language it was. Then
    it makes new columns. One is the Textblob of all the words in the text,
    and another is the textblob.words."""
    text_list = []
    ext_list = []
    for subdir, dirs, files in os.walk(dir_path):
        for name in files:
            if name.endswith((extensions)):
                ext_list.append(grab_extension(name))
                with open(os.path.join(subdir, name),\
                errors="surrogateescape") as f:
                    text_list.append(f.read())
    corpus_df = pd.DataFrame({"Language": ext_list, "Text" : text_list})
    corpus_df["Textblob"] = corpus_df.Text.apply((lambda x: TextBlob(x).words))
    corpus_df["Textblob letters"] = corpus_df.Text.apply((lambda x:\
                                                          TextBlob(x)))
    return corpus_df


def grab_extension(file):
    """Takes the extension and finds the language that is related to that
    language."""
    for lang in prog_langs.keys():
        for ext in prog_langs[lang]:
            if file.endswith(ext):
                return lang
