import traverse_folders as tf
from learner import Learner

if __name__ == '__main__':
    """ Read in files to use as training data. """
    #training_set = tf.build_training_set()
    java1 = "guess_lang/data/bench/knucleotide/knucleotide.java"
    java2 = "guess_lang/data/bench/knucleotide/knucleotide.java-2.java"
    perl1 = "guess_lang/data/bench/knucleotide/knucleotide.perl"
    perl2 = "guess_lang/data/bench/knucleotide/knucleotide.perl-2.perl"

    learner = Learner()

    
    learner.analyze(perl1)
