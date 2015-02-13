import traverse_folders as tf
from learner import Learner
from classifier import Classifier



if __name__ == '__main__':
    """ Read in files to use as training data. """
    training_set = tf.build_train_set("guess_lang/data/")

    learner = Learner()

    """ Build the DataFrame of features"""
    for code,language in training_set:
        learner.train(code, language)

    """ Read in files to use as testing data. """
    testing_set = tf.build_test_set("guess_lang/final-test/")
    answers = tf.get_answers("guess_lang/test.csv")
    testing_set = sorted(testing_set, key = lambda x: x[0])
    classifier = Classifier(learner.training_df)


    print("Decision Tree")
    correct = 0
    for test_number,test in testing_set:
        analysis = learner.analyze(test)
        decision = classifier.decision_tree(analysis)[0].lower()
        if decision == (answers[test_number]):
            correct += 1
        print(test_number, ": ", decision)
    print("Score: {}".format(correct/32))


    print("Random Forest")
    correct = 0
    for test_number,test in testing_set:
        analysis = learner.analyze(test)
        decision = classifier.random_forest(analysis)[0].lower()
        if decision == (answers[test_number]):
            correct += 1
        print(test_number, ": ", decision)
    print("Score: {}".format(correct/32))
