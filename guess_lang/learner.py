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
        self.features = [self.dollar_ratio]       # A List of feature functions
        # When I initialize the columns of features, run each function with
        # arguments.  This returns a string representation to use in printing. 
        for column in self.features:
            self.features_df[column()] = pd.Series(index=self.features_df.index)

    def analyze(self,code_path):
        code_count = (self.features_df.index)
        code = open(code_path).read()
        for feature in self.features:

            column, value = feature(code)
            #self.features_df[code_count,column] = value
        print(self.features_df)


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
        return ("dollar_count", dollar_count/len(code))
