import os
import re
import pickle
import parser


def load_classifier(test_file="random_forest.dat", key="key.txt"):
    with open(test_file, "rb") as saved_classifier:
        classifier = pickle.load(saved_classifier)
    return classifier


def prepare_file(file_location):
    return parser.parse_and_score(file_location)


def test_file(classifier, test_data):
    return classifier.predict(test_data)


if __name__ == '__main__':
    file_location = input("Enter file location: ")
    classifier = load_classifier()
    data = prepare_file(file_location)
    results = test_file(classifier, data)
    print(results[0])
