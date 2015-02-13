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
        self.features = [self.dollar_ratio, self.semicolon_ratio,self.let_ratio,
                         self.bracket_ratio, self.double_semicolon_ratio,
                         self.defn_ratio, self.include_ratio]
        self.newfeatures = ['$', ';', 'let', '{', ';;', 'defn', 'include']
        # When I initialize the columns of features, run each function with
        # arguments.  This returns a string representation to use in printing.
        for column in self.features:
            self.training_df[column()] = pd.Series(index=self.training_df.index)

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
            column, value = feature(code)
            self.training_df.loc[code_count,column] = value

    def analyze(self, code_path):
        try:
            code = open(code_path).read()
        except:
            print("ERROR in testing: {}".format(code_path))
        analysis = pd.DataFrame()
        for feature in self.features:
            column, value = feature(code)
            analysis.loc[0,column] = value
        return analysis

    """ Feature Functions:
    Each function returns a tuple.
    A string representation of the function and the value to be added. """

    def dollar_ratio(self,code=None):
        if code == None:
            return "dollar_ratio"
        dollar_count = 0
        for char in code:
            if char == '$':
                dollar_count += 1
        return ("dollar_ratio", dollar_count/len(code))

    def semicolon_ratio(self,code=None):
        if code == None:
            return "semicolon_ratio"
        semicolon_count = 0
        for char in code:
            if char == ';':
                semicolon_count += 1
        return ("semicolon_ratio", semicolon_count/len(code))

    def let_ratio(self,code=None):
        if code == None:
            return "let_ratio"
        let_count = len(list(re.finditer(r' (let) ',code)))
        return ("let_ratio", let_count/len(code))

    def bracket_ratio(self,code=None):
        if code == None:
            return "bracket_ratio"
        bracket_count = 0
        for char in code:
            if char == '{':
                bracket_count += 1
        return ("bracket_ratio", bracket_count/len(code))

    def double_semicolon_ratio(self,code=None):
        if code == None:
            return "double_semicolon_ratio"
        double_count = len(list(re.finditer(r'(;;)',code)))
        return ("double_semicolon_ratio", double_count/len(code))

    def defn_ratio(self,code=None):
        if code == None:
            return "defn_ratio"
        defn_count = len(list(re.finditer(r'(defn)',code)))
        return ("defn_ratio", defn_count/len(code))

    def include_ratio(self,code=None):
        if code == None:
            return "include_ratio"
        include_count = len(list(re.finditer(r'(include) ',code)))
        return ("include_ratio", include_count/len(code))

    def get_ratio(self, code, snip, title):
        if code == None:
            return title
        regex = r'('+re.escape(snip)+r')'
        count = len(list(re.finditer(regex, code)))
        return (title, (len(snip)*count)/len(code))
