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

raw_file_list = [filename for filename in
                 glob.iglob(os.path.join('corpus/bench', '*', '*'))
                 if os.path.splitext(filename)[1] in file_types.keys()]

feature_list = [('parent_count', "[()]"),
                ('double_colon', "::"),
                ('let_exists', r"\blet\b"),
                ('less_minus', "((\<\-))"),
                ('paren_star', "(\(\*|\*\))"),
                ('def_exists', r"\bdef\b"),
                ('end_exists', r"\bend\b"),
                ('curly_bracket', "[\{\}]"),
                ('slash_star_star', "\/\*\*"),
                ('forward_slash', "//"),
                ('var_exists', r"\bvar\b"),
                ('star_count', r"\b\*\b"),
                ('dollar_sign', r"\$"),
                ('val_exists', r"\bval\b")]


class Corpus():

    def __init__(self, file_list=[]):
        self.file_list = file_list

    def read_process_file(self, file_name):
        with open(file_name) as f:
            return f.read()

    def build_dataframe(self, snippet=True):
        raw_text = [self.read_process_file(file) for file in self.file_list]

        if snippet:
            a_dataframe = pd.DataFrame(raw_text, columns=['raw_text'])
        else:
            a_dataframe = pd.DataFrame([file_types[os.path.splitext(file)[1]]
                                        for file in self.file_list],
                                       columns=['file_type'])

            a_dataframe['hit_num'] = a_dataframe['file_type'].map(hit_num)
            a_dataframe['raw_text'] = raw_text

        return a_dataframe

    def feat_lookup(self, regex, a_dataframe):
        return [(len(re.findall(regex, a_row))/len(a_row))
                for a_row in a_dataframe['raw_text']]

    def feature_breakout(self, a_df):

        for name, regex in feature_list:
            a_df[name] = self.feat_lookup(regex, a_df)

        return a_df

    def compl_df_build(self, snippet=True):
        a_df = self.build_dataframe(snippet)
        a_df = self.feature_breakout(a_df)
        cleaned_df = self.clean_df(a_df, snippet)
        return cleaned_df

    def clean_df(self, a_df, snippet):
        cleaned_df = a_df.drop(['raw_text'], axis=1)

        if not snippet:
            cleaned_df = cleaned_df.drop(['file_type'], axis=1)

        return cleaned_df
