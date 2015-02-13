import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import re


class Learner:
    """  A learner builds a dataframe of features to train on.
    When a new file is input, add a new row onto the dataframe.
    Loop through the list of features, which will fill in the
    corresponding columns.
    Each row will be a piece of code.  """

    def __init__(self):
        self.features_df = pd.DataFrame()
        # A List of feature functions
        self.features = [self.dollar_ratio, self.semicolon_ratio,self.let_ratio,
                         self.bracket_ratio]
        # When I initialize the columns of features, run each function with
        # arguments.  This returns a string representation to use in printing.
        for column in self.features:
            self.features_df[column()] = pd.Series(index=self.features_df.index)

    def __str__(self):
        return str(self.features_df)

    def analyze(self,code_path, language):
        code_count = len(self.features_df.index)
        try:
            code = open(code_path).read()
        except:
            print("ERROR: {}".format(code_path))
            print("{} files read successfully".format(code_count-1))
        self.features_df.loc[code_count,"class"] = language
        for feature in self.features:
            column, value = feature(code)
            self.features_df.loc[code_count,column] = value


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
