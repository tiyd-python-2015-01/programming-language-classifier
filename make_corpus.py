import glob


prog_lang = {"clojure": [".clj", ".cljs", ".edn", ".clojure"],
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
import os
def get_files():
    text_list = []
    ext_list =
    for subdir, dirs, files in os.walk("training/benchmarks/benchmarksgame/bench/"):
        for name in files:
            if name.endswith((extensions)):

                with open(os.path.join(subdir, name)) as f:
                    my_list.append(f.read())


def grab_extension(file):
    for lang in prog_land.keys():
        for ext in prog_land[lang]
            if file.endswith(ext):
                return lang


extensions = tuple(prog_lang.values())
