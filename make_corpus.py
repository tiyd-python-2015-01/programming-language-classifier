import glob




prog_lang = {"clojure": [".clj", ".cljs", ".edn"],
             "haskell" : [".hs", ".lhs"],
             "java": [".java", ".jar"],
             "javascript": [".js"],
             "ocaml": [".ml"],
             "perl" : [".pl", ".pm", ".t", ".pod"],
             "php" : [".php", ".phtml", ".php4", ".php3", ".php5", ".phps"],
             "python" : [".py", ".py", ".pyw", ".pyc", ".pyo", ".pyd"],
             "ruby" : ["rb", ".rbw"".rb"],
             "scala" : [".scala"],
             "scheme" : [".scm", ".ss"],
             "tcl" : [".tcl"]
             }

extensions = tuple(prog_lang.values())
