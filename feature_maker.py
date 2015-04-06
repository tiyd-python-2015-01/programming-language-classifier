import pandas as pd
import re


def find_percent_word(feature_list, dataframe):
    for feature in feature_list:
        def temp_fn(word_list):
            counter = 0
            for word in word_list:
                if word == feature:
                    counter += 1
            return counter/len(word_list)
        dataframe[feature] = dataframe["Textblob"].apply(temp_fn)


def find_percent_character(feature_list, dataframe):
    for feature in feature_list:
        def temp_fn(character_list):
            counter = 0
            for character in character_list:
                if character == feature:
                    counter += 1
            return counter/len(character_list)
        dataframe[feature] = dataframe["Textblob letters"].apply(temp_fn)


def find_percent_special_chars(special_chars, dataframe):
    for feature in special_chars:
        def temp_fn(text):
            counter = len(re.findall(feature, text))
            return counter/len(text.split())
        dataframe[feature] = dataframe["Text"].apply(temp_fn)


def add_to_df(dataframe):
    common_words =['Object', 'var', 'try', 'except', 'class', 'return',
                   'self', 'public', 'static', 'Body', 'val', 'defn',
                   'def', 'end', 'each', 'let', 'define', 'printf',
                   "function", "echo", "global", "foreach", "elif",
                   "data", "move", "where"]
    common_chars = ["!", "(", ")", ";", ":", "$", "@","[", "]", "|", "{", "}"]
    special_chars = ["=>", "->", "php"]
    find_percent_word(common_words, dataframe)
    find_percent_character(common_chars, dataframe)
    find_percent_special_chars(special_chars, dataframe)
