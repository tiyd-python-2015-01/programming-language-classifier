import glob
import os
import pandas as pd
import re


file_types = {'.clj': 'clojure',
'.cljs': 'clojure',
'.clojure': 'clojure',
'.edn': 'clojure',
'.hs': 'haskell',
'.lhs': 'haskell',
'.ghc': 'haskell',
'.java': 'java',
'.class': 'java',
'.js': 'javascript',
'.javascript': 'javascript',
'.ml': 'ocaml',
'.mli': 'ocaml',
'.ocaml': 'ocaml',
'.perl': 'perl',
'.php': 'php',
'.phtml': 'php',
'.php3': 'php',
'.php4': 'php',
'.php5': 'php',
'.phps': 'php',
'.python3': 'python',
'.python2': 'python',
'.py': 'python',
'.jruby': 'ruby',
'.scala': 'scala',
'.racket': 'scheme',
'.scm': 'scheme',
'.ss': 'scheme',
'.clojure': 'clojure'}

hit_num = {"clojure": "1",
"haskell": "2",
"java": "3",
"javascript": "4",
"ocaml": "5",
"perl": "6",
"php": "7",
"python": "8",
"ruby": "9",
"scala": "10",
"scheme": "11"}

raw_file_list = [filename
                 for filename in glob.iglob(os.path.join('corpus/bench',
                                                         '*', '*'))
                 if os.path.splitext(filename)[1] in file_types.keys()]


class Corpus():


    def read_process_file(self, file_name):
        with open(file_name) as f:
            return f.read()

    def parenthesis_count(self, a_string):
        return len(re.findall(r'[()]', a_string)) / len(a_string)

    def build_dataframe(self):
        a_dataframe = pd.DataFrame([file_types[os.path.splitext(file)[1]]
                                    for file
                                    in raw_file_list], columns=['file_type'])
        a_dataframe['hit_num'] = a_dataframe['file_type'].map(hit_num)
        raw_text = [self.read_process_file(file) for file in raw_file_list]
        a_dataframe['raw_text'] = raw_text

        return a_dataframe

    def feature_breakout(self, a_dataframe):

        a_dataframe['paren_count'] = [self.parenthesis_count(row)
                                      for row in a_dataframe['raw_text']]
        return a_dataframe


    def compl_df_build(self):
        corpus = self.build_dataframe()
        corpus = self.feature_breakout(corpus)
        return corpus
