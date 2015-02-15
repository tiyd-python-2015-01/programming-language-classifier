import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re


class Learner:
    """  A learner builds a dataframe of features to train on.
    When a new file is input, add a new row onto the dataframe.
    Loop through the list of features, which will fill in the
    corresponding columns.
    Each row will be a piece of code.  """

    def __init__(self):
        self.training_df = pd.DataFrame()
        # A List of feature functions

        self.features = [r'\$[\D]', r'[^;];[^.]', r';;[^;]', r';;;',
                         r'include', r'let', r'{[^-]', r'{-',
                         r'import', r'var', r'@', r'#', r'=>', r'js\.', r'/\*',
                         r'->', '\(\*', r'|[^|]', r'& args', r'<?php'
                         r'type', r'final', r'"""', r'<!', r'my', r'::',
                         r'__name__', r'defn ', r'def ',
                         r'__init__', r'=begin', r'puts', r'===', r'clojure\.',
                         r'[^/]\*', r'haskell', r'__str__', r'\(function[ ]?\(']
        # When I initialize the columns of features, run each function with
        # arguments.  This returns a string representation to use in printing.
        for column in self.features:
            self.training_df[self.get_ratio(snip=column)] = \
                                        pd.Series(index=self.training_df.index)

    def __str__(self):
        return str(self.training_df)

    def train(self,code_path, language):
        code_count = len(self.training_df.index)
        try:
            code = open(code_path).read()
        except:
            print("ERROR in training: {}".format(code_path))
            print("{} files read successfully".format(code_count-1))
        self.training_df.loc[code_count,"class"] = language
        for feature in self.features:
            column, value = self.get_ratio(code=code,snip=feature)
            self.training_df.loc[code_count,column] = value

    def analyze(self, code_path):
        try:
            code = open(code_path).read()
        except:
            print("ERROR in testing: {}".format(code_path))
        analysis = pd.DataFrame()
        for feature in self.features:
            column, value = self.get_ratio(code=code,snip=feature)
            analysis.loc[0,column] = value
        return analysis

    """ Feature Functions:
    Each function returns a tuple.
    A string representation of the function and the value to be added. """

    def get_ratio(self, code=None, snip=None):
        title = "{}_ratio".format(snip)
        if code == None:
            return title
        #regex = r'('+re.escape(snip)+r')'
        regex = r'(' + snip + r')'
        count = len(list(re.finditer(regex, code, re.MULTILINE)))
        return (title, (len(snip)*count)/len(code))
