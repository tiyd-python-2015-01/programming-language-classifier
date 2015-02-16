import re
import os
from os.path import isfile, join
import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from open_parse import *
import pickle

if __name__ == '__main__':

    path = ("/Users/chameleonsrock/ironyard/sandbox"
            "/programming-language-classifier/bench")

    train = open_and_parse(path)
    file_paths = get_filepaths(path)
    train['extension'] = [os.path.splitext(fp)[-1].lower() for fp in file_paths]
    train['Language'] = train.extension.map(get_lang)

    train_data = train.drop(['extension', 'Language', 'Snippet'], axis=1)
    results = train['Language'].values

    X_train, X_test, y_train, y_test = train_test_split(train_data,
                                                        results,
                                                        test_size=0.4,
                                                        random_state=0)

    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train)

    with open("/Users/chameleonsrock/ironyard/sandbox"
              "/programming-language-classifier"
              "/rf_programming.dat", "wb") as f:
        pickle.dump(classifier, f)
