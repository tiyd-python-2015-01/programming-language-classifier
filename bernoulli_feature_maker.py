import pandas as pd
import re


def find_word(feature_list, dataframe):
    for feature in feature_list:
        def temp_fn(word_list):
            for word in word_list:
                if word == feature:
                    return 1
            return 0
        dataframe[feature] = dataframe["Textblob"].apply(temp_fn)


def find_character(feature_list, dataframe):
    for feature in feature_list:
        def temp_fn(character_list):
            for character in character_list:
                if character == feature:
                    return 1
            return 0
        dataframe[feature] = dataframe["Textblob letters"].apply(temp_fn)


def find_special_chars(special_chars, dataframe):
    for feature in special_chars:
        def temp_fn(text):
            counter = len(re.findall(feature, text))
            if counter > 0:
                return 1
            else:
                return 0
        dataframe[feature] = dataframe["Text"].apply(temp_fn)


def b_add_to_df(dataframe):
    common_words =['Object', 'var', 'try', 'except', 'class', 'return',
                   'self', 'public', 'static', 'Body', 'val', 'defn',
                   'def', 'end', 'each', 'let', 'define', 'printf',
                   "function", "echo", "global", "foreach", "elif",
                   "data", "move", "where"]
    common_chars = ["!", "(", ")", ";", ":", "$", "@","[", "]", "|", "{", "}"]
    special_chars = ["=>", "->", "php"]
    find_word(common_words, dataframe)
    find_character(common_chars, dataframe)
    find_special_chars(special_chars, dataframe)
