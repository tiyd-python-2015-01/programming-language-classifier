import os
import pandas as pd

filename_dict = {".clj":"Clojure",
                 ".cljs": "Clojure",
                 ".edn": "Clojure",
                 ".clojure": "Clojure",
                 ".hs": "Haskell",
                 ".lhs": "Haskell",
                 ".java": "Java",
                 ".class": "Java",
                 ".jar": "Java",
                 ".js": "Javascript",
                 ".javascript": "Javascript",
                 ".ocaml": "OCaml",
                 ".ml": "OCaml",
                 ".pl": "Perl",
                 ".pm": "Perl",
                 ".t": "Perl",
                 ".pod": "Perl",
                 ".php": "PHP",
                 ".perl": "Perl",
                 ".phtml": "PHP",
                 ".php4": "PHP",
                 ".php3": "PHP",
                 ".php5": "PHP",
                 ".phps": "PHP",
                 ".py": "Python",
                 ".pyw": "Python",
                 ".pyc": "Python",
                 ".pyo": "Python",
                 ".pyd": "Python",
                 ".python3": "Python",
                 ".Python2": "Python",
                 ".rb": "Ruby",
                 ".rbw": "Ruby",
                 ".jruby": "Ruby",
                 ".scala": "Scala",
                 ".scm": "Scheme",
                 ".ss": "Scheme",
                 ".tcl": "Tcl",
                 ".racket": "Scheme",
                 ".ghc": "Haskell"}

def tuple_maker(adict):
    lista = []
    for key in adict:
        lista.append(key)
    tup = tuple(lista)
    return tup

def code_sucker():
    codelist = []
    for subdir, dirs, files in os.walk("bench/"):
        for fname in files:
            if fname.endswith(tuple_maker(filename_dict)):
                #print(fname)
                with open(os.path.join(subdir, fname)) as current_file:
                    codelist.append(current_file.read())
    return codelist

def type_getter():
    rootDir = 'bench'
    typelist = []
    for subdir, dirs, files in os.walk(rootDir):
        for fname in files:
            #print('\t%s' % fname)
            name, extension = os.path.splitext(fname)
            if extension in filename_dict:
                #print(filename_dict[extension])
                typelist.append(filename_dict[extension])
    return typelist

def tcode_sucker():
    codelist = []
    for subdir, dirs, files in os.walk("test/"):
        for fname in files:
            with open(os.path.join(subdir, fname)) as current_file:
                codelist.append(current_file.read())
    return codelist
