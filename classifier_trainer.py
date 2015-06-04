import pandas as pd
from sklearn.naive_bayes import GaussianNB
from make_corpus import get_corpus
from feature_maker import add_to_df
import pickle


def gaussian_classifier():
    df = get_corpus("training/benchmarks/benchmarksgame/bench/")
    add_to_df(df)
    classifier = GaussianNB()
    classifier = classifier.fit(df.loc[0::,'Object':"php"], df.loc[0::,"Language"])
    return classifier

def pickle_classifier(item):
    with open('language_detector.pkl', 'wb') as fout:
        pickle.dump(classifier, fout)

if __name__ == '__main__':
    classifier = gaussian_classifier()
    pickle_classifier(classifier)
