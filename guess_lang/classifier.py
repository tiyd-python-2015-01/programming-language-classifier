import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier



class Classifier:

    def __init__(self, training_df):
        self.training_df = training_df
        self.testing_df = pd.DataFrame()

    def __str__(self):
        return str(self.testing_df)

    def decision_tree(self,testframe):
        code_count = len(self.testing_df.index)
        tree = DecisionTreeClassifier()
        features = self.training_df.ix[:,:-1]
        classes = self.training_df.ix[:,-1]
        classifier = tree.fit(features,classes)
        prediction = classifier.predict(testframe.ix[:,:])
        return prediction

    def random_forest(self,testframe):
        code_count = len(self.testing_df.index)
        tree = RandomForestClassifier()
        features = self.training_df.ix[:,:-1]
        classes = self.training_df.ix[:,-1]
        classifier = tree.fit(features,classes)
        prediction = classifier.predict(testframe.ix[:,:])
        return prediction
