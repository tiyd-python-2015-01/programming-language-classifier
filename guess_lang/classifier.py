import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import LinearSVC
from sklearn.cluster import KMeans

LANGUAGES = ['Clojure','Haskell','Java','JavaScript','OCaml',
             'Perl','PHP','Python','Ruby','Scala','Scheme','Tcl']

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
        prediction = classifier.predict(testframe)
        return prediction

    def random_forest(self,testframe):
        code_count = len(self.testing_df.index)
        features = self.training_df.ix[:,:-1]
        classes = self.training_df.ix[:,-1]
        tree = RandomForestClassifier(max_features='sqrt')
        classifier = tree.fit(features,classes)
        prediction = classifier.predict(testframe)
        return prediction

    def extreme_random_forest(self,testframe):
        code_count = len(self.testing_df.index)
        features = self.training_df.ix[:,:-1]
        classes = self.training_df.ix[:,-1]
        tree = ExtraTreesClassifier()
        classifier = tree.fit(features,classes)
        prediction = classifier.predict(testframe)
        return prediction

    def linear_svc(self,testframe):
        code_count = len(self.testing_df.index)
        tree = LinearSVC(loss='l1')
        features = self.training_df.ix[:,:-1]
        classes = self.training_df.ix[:,-1]
        classifier = tree.fit(features,classes)
        prediction = classifier.predict(testframe)
        return prediction



    def cluster(self,testframe):
        """ Clustering is unsupervised learning so what if we cluster
        the codes and then run each cluster through random forest
        or another supervised algorithm in order to actually identify each.
        """
        code_count = len(self.testing_df.index)
        cluster = KMeans(12)
        #cluster.set_params(LANGUAGES)
        features = self.training_df.ix[:,:-1]
        classes = self.training_df.ix[:,-1]
        try:
            classifier = cluster.fit(features)#,classes)
        except:
            print(features)
            print(classes)

        prediction = classifier.predict(testframe)
        print(prediction)
        return prediction
