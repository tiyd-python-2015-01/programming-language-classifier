import sys
import os
import pickle
import traverse_folders as tf
from learner import Learner
from classifier import Classifier
from sklearn.cluster import KMeans



if __name__ == '__main__':
    training_path = "guess_lang/data/"
    testing_path = "guess_lang/final-test/"
    single_file = False
    use_pickle = True

    if len(sys.argv) > 1:
        if sys.argv[1] == '-n':
            use_pickle = False
        else:
            testing_path = sys.argv[1]
            single_file = True

    learner_path = "learner.data"
    if os.path.isfile(learner_path) and use_pickle:
        learner_file = open(learner_path, 'rb')
        learner = pickle.load(learner_file)
        learner_file.close()
    else:
        """ Read in files to use as training data. """
        training_set = tf.build_train_set(training_path)
        learner = Learner()
        """ Build the DataFrame of features"""
        for code,language in training_set:
            learner.train(code, language)
        """ Read in files to use as testing data. """


    classifier_path = "classifier.data"
    if os.path.isfile(classifier_path) and use_pickle:
        classifier_file = open(classifier_path, 'rb')
        classifier = pickle.load(classifier_file)
        classifier_file.close()
    else:
        classifier = Classifier(learner.training_df)

    testing_set = tf.build_test_set(testing_path)
    answers = tf.get_answers("guess_lang/test.csv")
    testing_set = sorted(testing_set, key = lambda x: x[0])


    # print("Decision Tree")
    # correct = 0
    # for test_number,test in testing_set:
    #     analysis = learner.analyze(test)
    #     decision = classifier.decision_tree(analysis)[0].lower()
    #     if decision == (answers[test_number]):
    #         correct += 1
    #     #print(test_number, ": ", decision)
    # print("Score: {}".format(correct/32))


    print("Random Forest")
    correct = 0
    for test_number,test in testing_set:
        analysis = learner.analyze(test)
        decision = classifier.random_forest(analysis)[0].lower()
        if decision == (answers[test_number]):
            correct += 1
        if single_file:
            print(test_number, ": ", decision)
        else:
            print(test_number, ": ", decision, "\tCorrect: ",answers[test_number])
    if not single_file:
        print("Score: {}".format(correct/32))

    print("Extremely Random Forest")
    correct = 0
    for test_number,test in testing_set:
        analysis = learner.analyze(test)
        decision = classifier.extreme_random_forest(analysis)[0].lower()
        if decision == (answers[test_number]):
            correct += 1
        if single_file:
            print(test_number, ": ", decision)
        else:
            print(test_number, ": ", decision, "\tCorrect: ",answers[test_number])
    if not single_file:
        print("Score: {}".format(correct/32))

    # print("Linear SVC")
    # correct = 0
    # for test_number,test in testing_set:
    #     analysis = learner.analyze(test)
    #     decision = classifier.linear_svc(analysis)[0].lower()
    #     if decision == (answers[test_number]):
    #         correct += 1
    #     #print(test_number, ": ", decision)
    # print("Score: {}".format(correct/32))

    # print("Cluster")
    # correct = 0
    # for test_number,test in testing_set:
    #     analysis = learner.analyze(test)
    #     decision = classifier.cluster(analysis)[0]
    #     if decision == (answers[test_number]):
    #         correct += 1
    #     #print(test_number, ": ", decision)
    # print("Score: {}".format(correct/32))
    if not os.path.isfile(learner_path):
        output = open(learner_path, 'wb')
        pickle.dump(learner, output, protocol=2)
        output.close()
    if not os.path.isfile(classifier_path):
        output = open(classifier_path, 'wb')
        pickle.dump(classifier, output, protocol=2)
        output.close()
