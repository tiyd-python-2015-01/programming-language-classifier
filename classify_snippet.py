#!/usr/bin/env python
import pickle
import os
import os.path
import pandas as pd
import nltk
import re
import numpy as np
from textblob import TextBlob as tb
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import lang_orig as lg
import sys


def select_features_new_test(word_list, final):
        final_list = {}
        for key in final:
            found = 0
            for word, score in word_list:
                if word == key:
                        found = score
                        break
            final_list[key] = round(found, 5)
        return final_list


def setup_data():
    cls = pickle.load(open("model.p", "rb"))
    final_features = pickle.load(open("features.p", "rb"))
    return final_features, cls


def return_tokens(code):
    tokens = nltk.word_tokenize(code)
    return tb(' '.join(tokens))


def create_vectors_new_test(features):
    vec = DictVectorizer()
    return vec.fit_transform(features).toarray()


def predict(code, model, final_features):
    token_blob = return_tokens(code)
    word_list = lg.calculate_scores(token_blob)
    features = select_features_new_test(word_list, final_features)
    new_x = create_vectors_new_test(features)
    predicted = model.predict(new_x)
    predicted_probs = model.predict_proba(new_x)
    return predicted, predicted_probs


def print_probabilities(probas, model):
    print("Probabilites for my prediction:")
    for ind in range(len(probas[0])):
        print(model.classes_[ind], ':', round(probas[0][ind], 2))


def read_code():
    file_name = sys.argv[1]
    myfile = open(file_name)
    myfile_content = myfile.read()
    return myfile_content


model_features, model = setup_data()
code = read_code()
predicted, predicted_probs = predict(code, model, model_features)
print("I think this code is:{}".format(predicted[0]))
print_probabilities(predicted_probs, model)
