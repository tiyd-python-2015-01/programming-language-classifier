import os
import re
import sys
import pickle
import parser


def load_classifier(test_file="random_forest.dat"):
    with open(test_file, "rb") as saved_classifier:
        classifier = pickle.load(saved_classifier)
    return classifier


def prepare_file(file_location):
    return parser.parse_and_score(file_location)


def test_file(classifier, test_data):
    return classifier.predict(test_data)


def get_probabilities(classifier, test_data):
    return classifier.predict_proba(test_data).tolist()[0]

if __name__ == '__main__':
    classifier = load_classifier()
    classes = classifier.classes_.tolist()
    data = prepare_file(sys.argv[1])
    results = test_file(classifier, data)
    probabilities = get_probabilities(classifier, data)
    print("Programming Language Identification Results:\n")
    for index, item in enumerate(classes):
        print("{}: {}".format(item, probabilities[index]))
    print("\nBest Guess: {}".format(results[0]))
