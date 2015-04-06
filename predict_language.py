from bernoulli_feature_maker import b_add_to_df
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
    langs =["Clojure", "Haskell", "Java", "JavaScript", "Ocaml", "Perl",
            "Php", "Python", "Ruby", "Scala", "Scheme"]
    prob_dict = {}
    counter = 0
    for prob in probs[0]:
        prob_dict[langs[counter]] = prob
        counter += 1
    sorted_dict = Counter(prob_dict)
    top_three = sorted_dict.most_common(3)
    first_lang, first_num = top_three[0]
    second_lang, second_num = second = top_three[1]
    third_lang, third_num = top_three[2]
    print("Most likely languages...\n",
          "1.{}: {}%\n".format(first_lang, round(first_num, 3) * 100),
          "2.{}: {}%\n".format(second_lang, round(second_num, 3) * 100),
          "3.{}: {}%".format(third_lang, round(third_num, 3) * 100))


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

if __name__ == '__main__':
    test_file = sys.argv[1]
    make_prediction(test_file)
