import pandas as pd
from sklearn.naive_bayes import BernoulliNB
from make_corpus import get_corpus
from bernoulli_feature_maker import b_add_to_df
import pickle


def bernoulli_classifier():
    df = get_corpus("training/benchmarks/benchmarksgame/bench/")
    b_add_to_df(df)
    classifier = BernoulliNB()
    classifier = classifier.fit(df.loc[0::,'Object':"php"], df.loc[0::,"Language"])
    return classifier

def pickle_classifier(item):
    with open('language_detector.pkl', 'wb') as fout:
        pickle.dump(classifier, fout)

if __name__ == '__main__':
    classifier = bernoulli_classifier()
    pickle_classifier(classifier)
