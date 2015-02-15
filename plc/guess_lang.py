from data_load import*
from features import*
from classifier import*

from sklearn.naive_bayes import GaussianNB

import os
import pandas as pd
import re
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

word_list = ['let', 'end', 'defn', 'function', 'fun', 'return', 'def', 'return', 'check', 'make', '->', '.format',
             'define', '::', 'done', 'type', 'rescue', 'print', 'elif', 'clone', 'display', '$format', 'echo', 'str',
             'join', '&&', 'val', 'Nil', 'object', '<-', '--', 'lambda', 'var', '//', 'tmpl', 'public function',
             'stdlib', '=>', 'final', 'case', 'impl']
symbol_list = ['$', '^', ',', ';', '&', '|', '!', '*', '@', '#']
endings = ['end', ')', '}']

def data_frame_generator():
    codelist = code_sucker()
    typelist = type_getter()
    df = pd.DataFrame(typelist, index=range(386))
    df.columns = ["Language"]
    df["Code"] = codelist
    df['Language'] = df.Language.apply(lambda x:x.lower())
    for string in word_list:
        def sub_function(code):
            x = string_ratio(string, code)
            return x
        df[string] = df.Code.apply(sub_function)
    for char in symbol_list:
        def sub_function2(code):
            y = character_ratio(code, char)
            return y
        df[char] = df.Code.apply(sub_function2)
    for ending in endings:
        def sub_function3(code):
            z = string_end(ending, code)
            return z
        df['_' + ending] = df.Code.apply(sub_function3)
    return df

def x_data_frame_generator():
    test_list = []
    with open(args.filename) as test_file:
        test_list.append(test_file.read())
    df = pd.DataFrame(test_list, index=range(1), columns=['Code'])
    for string in word_list:
        def sub_function(code):
            x = string_ratio(string, code)
            return x
        df[string] = df.Code.apply(sub_function)
    for char in symbol_list:
        def sub_function2(code):
            y = character_ratio(code, char)
            return y
        df[char] = df.Code.apply(sub_function2)
    for ending in endings:
        def sub_function3(code):
            z = string_end(ending, code)
            return z
        df['_' + ending] = df.Code.apply(sub_function3)
    return df


def probability_display(df):
    n = gauss.predict_proba(xdf.loc[:, 'let':])
    prob_list = n.tolist()[0]
    programs_list = ['Clojure', 'Haskell', 'Java', 'Javascript', 'Ocaml', 'Perl', 'Php', 'Python', 'Ruby', 'Scala', 'Scheme']
    percent = 0
    for item in prob_list:
        if item > percent:
            percent = item
            idx = prob_list.index(item)
    print("The code snippet is written in {}".format(programs_list[idx]))
    print("Confidence: {}%".format(percent*100))

if __name__ == "__main__":
    df = data_frame_generator()
    gauss = GaussianNB()
    x_train, y_train = create_train(df, word_list[0], 'Language')
    gauss.fit(x_train, y_train)
    xdf = x_data_frame_generator()
    probability_display(xdf)
