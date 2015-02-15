import sys
import os
import pickle
import traverse_folders as tf
from learner import Learner
from classifier import Classifier
from sklearn.cluster import KMeans


class Language_Guesser:

    def __init__(self):
        pass

if __name__ == '__main__':
    training_path = "guess_lang/data/"
    testing_path = "guess_lang/test/"
    single_file = False
    use_pickle = True

    """ Check for command-line arguments.  If -n, don't use pickled files. """
    if len(sys.argv) > 1:
        if sys.argv[1] == '-n':
            use_pickle = False
        else:
            testing_path = sys.argv[1]
            single_file = True
            try:
                if sys.argv[2] == '-n':
                    use_pickle = False
            except:
                pass

    """ If learner object has been pickled, load it.
        else, build the learner. (also check use_pickle arg) """
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
        for code, language in training_set:
            learner.train(code, language)

    """ If the classifier has been pickled, load it.
        Else build the classifier. (also check use_pickle arg) """
    classifier_path = "classifier.data"
    if os.path.isfile(classifier_path) and use_pickle:
        classifier_file = open(classifier_path, 'rb')
        classifier = pickle.load(classifier_file)
        classifier_file.close()
    else:
        classifier = Classifier(learner.training_df)

    """ Build the list of files to test from testing_path.
        If user input a specified file, open it and prepare it for test. """
    testing_set = tf.build_test_set(testing_path)
    answers = tf.get_answers("guess_lang/test.csv")
    testing_set = sorted(testing_set, key=lambda x: x[0])

    # print("Decision Tree")
    # correct = 0
    # for test_number,test in testing_set:
    #     analysis = learner.analyze(test)
    #     decision = classifier.decision_tree(analysis)[0].lower()
    #     if decision == (answers[test_number]):
    #         correct += 1
    #     if single_file:
    #         print(test_number, ": ", decision)
    #     else:
    #         print(test_number, ": ", decision,
    #               "\tCorrect: ", answers[test_number])
    # print("Score: {}".format(correct/32))

    # print("Random Forest")
    # correct = 0
    # for test_number, test in testing_set:
    #     analysis = learner.analyze(test)
    #     decision = classifier.random_forest(analysis)[0].lower()
    #     if decision == (answers[test_number]):
    #         correct += 1
    #     if single_file:
    #         print(test_number, ": ", decision)
    #     else:
    #         print(test_number, ": ", decision,
    #               "\tCorrect: ", answers[test_number])
    # if not single_file:
    #     print("Score: {}".format(correct/32))

    print("Extra Trees Random Forest")
    correct = 0
    for test_number, test in testing_set:
        analysis = learner.analyze(test)
        decision = classifier.extreme_random_forest(analysis)[0].lower()
        if decision == (answers[test_number]):
            correct_string = "Correct!"
            correct += 1
        else:
            correct_string = "Incorrect: {}".format(answers[test_number])
        if single_file:
            print(test_number, ": ", decision.title())
        else:
            print(str.zfill(str(test_number), 2), ": ",
                  str.rjust(decision.title(), 10),
                  "\t", correct_string)
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

    """ Pickle learner and classifier if they aren't already pickled.
        If user specified -n, pickle the new learner and classifier. """
    if not os.path.isfile(learner_path) or not use_pickle:
        output = open(learner_path, 'wb')
        pickle.dump(learner, output, protocol=2)
        output.close()
    if not os.path.isfile(classifier_path) or not use_pickle:
        output = open(classifier_path, 'wb')
        pickle.dump(classifier, output, protocol=2)
        output.close()
