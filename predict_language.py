from classifier_trainer import gaussian_classifier
from bernoulli_feature_maker import b_add_to_df
from get_test_df import get_tests
from feature_maker import add_to_df
from sklearn import metrics
from textblob import TextBlob
from collections import Counter
import pandas as pd
import sys
import pickle


def make_temp_df(text):
    """Creates a basic temporary Dataframe."""
    temp_df = pd.DataFrame({"Text": text})
    temp_df["Textblob"] = temp_df.Text.apply((lambda x: TextBlob(x).words))
    temp_df["Textblob letters"] = temp_df.Text.apply((lambda x: TextBlob(x)))
    b_add_to_df(temp_df)
    return temp_df


def present_percent(probs):
    probs = probs.tolist()
    print(type(probs))
    print(probs)
    langs =["clojure", "haskell", "java", "javascript", "ocaml", "perl",
            "php", "python", "ruby", "scala", "scheme"]
    prob_dict = {}
    counter = 0
    for prob in probs[0]:
        prob_dict[langs[counter]] = prob
        counter += 1
    sorted_dict = Counter(prob_dict)
    top_three = sorted_dict.most_common(3)
    print("Most likely languages...\n", "{}".format(top_three))


if __name__ == '__main__':
    test_file = sys.argv[1]
    text_list = []
    with open(test_file) as test_file:
        text = test_file.read()
        text_list.append(text)
    temp_df = make_temp_df(text_list)
    print(temp_df)
    file = open("language_detector.pkl",'rb')
    classifier = pickle.load(file)
    prediction = classifier.predict(temp_df.loc[0::,'Object':"php"])
    probability = classifier.predict_proba(temp_df.loc[0::,'Object':"php"])
    print(prediction)
    present_percent(probability)
