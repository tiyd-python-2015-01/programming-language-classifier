from bernoulli_feature_maker import b_add_to_df
from textblob import TextBlob
from collections import Counter
import pandas as pd
import sys
import pickle


languages =["Clojure", "Haskell", "Java", "JavaScript", "Ocaml", "Perl",
        "Php", "Python", "Ruby", "Scala", "Scheme"]

def make_temp_df(text):
    """Creates a basic temporary Dataframe."""
    temp_df = pd.DataFrame({"Text": text})
    temp_df["Textblob"] = temp_df.Text.apply((lambda x: TextBlob(x).words))
    temp_df["Textblob letters"] = temp_df.Text.apply((lambda x: TextBlob(x)))
    b_add_to_df(temp_df)
    return temp_df


def present_percent(probabilites):
    tuples = list(zip(languages, probabilites.tolist()[0]))
    sorted_list = sorted(tuples, key=lambda x: x[1], reverse=True)
    first_lang, first_num = sorted_list[0]
    second_lang, second_num = sorted_list[1]
    third_lang, third_num = sorted_list[2]
    print("Most likely languages...\n",
          "1. {}: {}%\n".format(first_lang, round(first_num * 100, 1)),
          "2. {}: {}%\n".format(second_lang, round(second_num * 100, 1)),
          "3. {}: {}%".format(third_lang, round(third_num * 100, 1)))
    return sorted_list




def make_prediction(test_file):
    text_list = []
    with open(test_file) as test_file:
        text = test_file.read()
        text_list.append(text)
    temp_df = make_temp_df(text_list)
    file = open("language_detector.pkl",'rb')
    classifier = pickle.load(file)
    prediction = classifier.predict(temp_df.loc[0::,'Object':"php"])
    probability = classifier.predict_proba(temp_df.loc[0::,'Object':"php"])
    print("I predict the language is: {}".format(prediction[0]))
    present_percent(probability)


def make_prediction_from_text(text):
    text_list = [text]
    temp_df = make_temp_df(text_list)
    file = open("language_detector.pkl",'rb')
    classifier = pickle.load(file)
    prediction = classifier.predict(temp_df.loc[0::,'Object':"php"])
    probability = classifier.predict_proba(temp_df.loc[0::,'Object':"php"])
    print("I predict the language is: {}".format(prediction[0]))
    present_percent(probability)

if __name__ == '__main__':
    text = sys.argv[1]
    make_prediction(text)
