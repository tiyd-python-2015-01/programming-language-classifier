import traverse_folders as tf
from learner import Learner

if __name__ == '__main__':
    """ Read in files to use as training data. """
    training_set = tf.build_training_set()
    java1 = "guess_lang/data/bench/knucleotide/knucleotide.java","Java"
    java2 = "guess_lang/data/bench/knucleotide/knucleotide.java-2.java","Java"
    perl1 = "guess_lang/data/bench/knucleotide/knucleotide.perl","Perl"
    perl2 = "guess_lang/data/bench/knucleotide/knucleotide.perl-2.perl","Perl"
    snippets = [java1,java2,perl1,perl2]
    learner = Learner()

    for code,language in training_set:
        learner.analyze(code,language)

    print(learner)
