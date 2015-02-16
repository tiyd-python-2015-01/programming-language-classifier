import numpy as np
import os
import re
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.metrics import (classification_report, f1_score, accuracy_score,
                             confusion_matrix)
from sklearn.ensemble import RandomForestClassifier
import pickle
import parser


def create_training_data():
    """Creates training data list and results list corresponding to the
    data list for training the classifier."""
    data_directory = "train_files/"

    filetype_dict = create_filetype_dict()
    filetype_list = list(set(value for key, value in filetype_dict.items()))
    training_data = []
    training_results = []

    for file in os.listdir(data_directory):
        fileext = re.findall(r"\w+\.?\w+?\.(\w+)", file)
        if fileext:
            if fileext[0] == "txt":
                continue
            filetype = filetype_dict[fileext[0]]
            training_results.append(filetype)
            training_data.append(parser.parse_and_score(data_directory + file))

    return training_data, training_results


def create_filetype_dict():
    """Read in file containing all known file extensions and their language
    and create a dictionary for lookup"""
    with open("train_files/extension_dict.txt") as filetype:
        filetype_data = filetype.readlines()
    filetype_list = []
    for line in filetype_data:
        filetype_list.extend(re.findall(r"(\w+), (\w+)", line))
    filetype_dict = {}
    for filetypes in filetype_list:
        key, value = filetypes
        filetype_dict[key] = value
    return filetype_dict


def split_data(data, results, test_size):
    """Splits the data into training and test data sets."""
    train_data, test_data, train_results, test_results = train_test_split(
        data, results, test_size=test_size, random_state=0)

    return train_data, test_data, train_results, test_results


def train_learner(train_data, train_results):
    """Fit the classifier to the training data."""
    learner = RandomForestClassifier(n_estimators=100, random_state=0)
    learner.fit(train_data, train_results)
    return learner


def test_learner(learner, test_data, test_results):
    """Test the classifier against the test data"""
    prediction = learner.predict(test_data)
    print(classification_report(test_results, prediction))
    print(confusion_matrix(test_results, prediction))
    print(f1_score(test_results, prediction))


def export_forest(forest):
    """Save the classifer as a pickle file for use in the predictor."""
    with open("random_forest.dat", "wb") as file:
        pickle.dump(max_train, file)


if __name__ == '__main__':
    data, results = create_training_data()
    train_data, test_data, train_results, test_results = split_data(data,
                                                                    results,
                                                                    0.2)
    trained_forest = train_learner(train_data, train_results)
    test_learner(trained_forest, test_data, test_results)

    max_train = train_learner(data, results)
    export_forest(max_train)
