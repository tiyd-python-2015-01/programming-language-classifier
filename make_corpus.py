import pandas as pd
import numpy as np
import os
from textblob import TextBlob


prog_langs = {"clojure": [".clj", ".cljs", ".edn", ".clojure"],
             "haskell" : [".hs", ".lhs", ".ghc"],
             "java": [".java", ".jar"],
             "javascript": [".js", ".javascript"],
             "ocaml": [".ml"],
             "perl" : [".pl", ".pm", ".t", ".pod"],
             "php" : [".php", ".phtml", ".php4", ".php3", ".php5", ".phps"],
             "python" : [".py", ".py", ".pyw", ".pyc", ".pyo", ".pyd", ".python3"],
             "ruby" : ["rb", ".rbw"],
             "scala" : [".scala"],
             "scheme" : [".scm", ".ss", ".racket"],
             "tcl" : [".tcl"]
             }


extensions = (".clj", ".cljs", ".edn", ".clojure",
             ".hs", ".lhs", ".ghc",".java", ".jar",
             ".js", ".javascript", ".ml", ".pl",
             ".pm", ".t", ".pod", ".php", ".phtml",
             ".php4", ".php3", ".php5", ".phps",
             ".py", ".pyw", ".pyc", ".pyo", ".pyd",
             ".python3", "rb", ".rbw", ".scala",
             ".scm", ".ss", ".racket", ".tcl")


def get_corpus(dir_path):
    text_list = []
    ext_list = []
    for subdir, dirs, files in os.walk(dir_path):
        for name in files:
            if name.endswith((extensions)):
                ext_list.append(grab_extension(name))
                with open(os.path.join(subdir, name)) as f:
                    text_list.append(f.read())
    corpus_df = pd.DataFrame({"Language": ext_list, "Text" : text_list})
    corpus_df["Textblob"] = corpus_df.Text.apply((lambda x: TextBlob(x).words))
    corpus_df["Textblob letters"] = corpus_df.Text.apply((lambda x: TextBlob(x)))
    return corpus_df


def grab_extension(file):
    for lang in prog_langs.keys():
        for ext in prog_langs[lang]:
            if file.endswith(ext):
                return lang
