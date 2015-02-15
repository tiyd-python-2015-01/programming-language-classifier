from classifier_trainer import gaussian_classifier
from get_test_df import get_tests
from feature_maker import add_to_df
from sklearn import metrics
import pickle



if __name__ == '__main__':
    file = open("language_detector.pkl",'rb')
    classifier = pickle.load(file)
    test_df = get_tests('test')
    add_to_df(test_df)
    predictions = classifier.predict(test_df.loc[0::,'Object':"php"])
    print(metrics.classification_report(test_df.loc[0::,"Language"], predictions))
    print(metrics.confusion_matrix(test_df.loc[0::,"Language"], predictions))
    print(metrics.f1_score(test_df.loc[0::,"Language"], predictions))
