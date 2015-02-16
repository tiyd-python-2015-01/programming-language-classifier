import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import LinearSVC
from sklearn.cluster import KMeans

LANGUAGES = ['Clojure', 'Haskell', 'Java', 'JavaScript', 'OCaml',
             'Perl', 'PHP', 'Python', 'Ruby', 'Scala', 'Scheme', 'Tcl']


class Classifier:

    def __init__(self, training_df):
        """ Uses the training data and builds a dataFrame for the test files.
        Classifiers are attributes of this class so that they can be saved
        through pickling.  We don't need to save the actual classifiers,
        only the results of each classifier's fit() method. """
        self.training_df = training_df
        self.testing_df = pd.DataFrame()
        self.dt_fit = None
        self.rf_fit = None
        self.et_fit = None
        self.lsvc_fit = None
        self.cl_fit = None

    def __str__(self):
        return str(self.testing_df)

    """ Each classification method is roughly the same.
    If a fit() attribute has not been loaded through pickling, build a new
    classifier, give it the features (all but the last column) and
    the class (the last column). Perform a fit()
    Make and return a prediction, given the testframe. """

    def decision_tree(self, testframe):
        code_count = len(self.testing_df.index)
        if not self.dt_fit:
            tree = DecisionTreeClassifier()
            features = self.training_df.ix[:, :-1]
            classes = self.training_df.ix[:, -1]
            self.dt_fit = tree.fit(features, classes)
        prediction = self.dt_fit.predict(testframe)
        return prediction

    def random_forest(self, testframe):
        code_count = len(self.testing_df.index)
        if not self.rf_fit:
            forest = RandomForestClassifier(n_estimators=15,
                                            criterion='gini',
                                            max_features=None)
            features = self.training_df.ix[:, :-1]
            classes = self.training_df.ix[:, -1]
            self.rf_fit = forest.fit(features, classes)
        prediction = self.rf_fit.predict(testframe)
        return prediction

    def extreme_random_forest(self, testframe):
        code_count = len(self.testing_df.index)
        if not self.et_fit:
            extra_trees = ExtraTreesClassifier(n_estimators=15,
                                               criterion='gini',
                                               max_features=None)
            features = self.training_df.ix[:, :-1]
            classes = self.training_df.ix[:, -1]
            self.et_fit = extra_trees.fit(features, classes)
        prediction = self.et_fit.predict(testframe)
        return prediction

    def linear_svc(self, testframe):
        code_count = len(self.testing_df.index)
        if not self.lsvc_fit:
            linear_svc = LinearSVC(loss='l1')
            features = self.training_df.ix[:, :-1]
            classes = self.training_df.ix[:, -1]
            self.lsvc_fit = linear_svc.fit(features, classes)
        prediction = self.lsvc_fit.predict(testframe)
        return prediction

    def cluster(self, testframe):
        """ Clustering is unsupervised learning so what if we cluster
        the codes and then run each cluster through random forest
        or another supervised algorithm in order to actually identify each.
        """
        code_count = len(self.testing_df.index)
        cluster = KMeans(12)
        # cluster.set_params(LANGUAGES)
        features = self.training_df.ix[:, :-1]
        classes = self.training_df.ix[:, -1]
        try:
            classifier = cluster.fit(features)  # ,classes)
        except:
            print(features)
            print(classes)

        prediction = classifier.predict(testframe)
        print(prediction)
        return prediction
