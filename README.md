There are 5 python files:

1- rosetta_scraper.py:  scrapes rosetta's web site for 60 examples of
code for each of the languages in this analysis

2- lang_orig.py: This is the code used to train the model and to select the model with best performance. The best performance was found to be
a decision tree with 160 features (representing the proportion of occurrence for the most used words including punctuation in the code)

3- classify.py: Tests the selected model with the new files provided. The model predicts the code correctly approx. 80% of the time.

4- classify_snippets.py: This file expects to receive the name of a file as argument and then prints the predicted language as well as the
probabilities for each language.

5- Model_Demonstration.ipynb shows how the model is used to predict the language for a given piece of code.

There are 2 objects saved with pickle: the model and the final features for the model.






****************************************************
# Classify code snippets into programming languages

## Description

Create a classifier that can take snippets of code and guess the programming language of the code.

## Objectives

### Learning Objectives

After completing this assignment, you should understand:

* Feature extraction
* Classification
* The varied syntax of programming languages

### Performance Objectives

After completing this assignment, you should be able to:

* Build a robust classifier

## Details

### Deliverables

* A Git repo called programming-language-classifier containing at least:
  * `README.md` file explaining how to run your project
  * a `requirements.txt` file
  * a suite of tests for your project

### Requirements  

* Passing unit tests
* No PEP8 or Pyflakes warnings or errors

## Normal Mode

### Getting a corpus of programming languages

Option 1: Get code from the [Computer Language Benchmarks Game](http://benchmarksgame.alioth.debian.org/). You can [download their code](https://alioth.debian.org/snapshots.php?group_id=100815) directly. In the downloaded archive under `benchmarksgame/bench`, you'll find many directories with short programs in them. Using the file extensions of these files, you should be able to find out what programming language they are.

Option 2: Scrape code from [Rosetta Code](http://rosettacode.org/wiki/Rosetta_Code). You will need to figure out how to scrape HTML and parse it. [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) is your best bet for doing that.

Option 3: Get code from GitHub somehow. The specifics of this are left up to you.

You are allowed to use other code samples as well.

**For your sanity, you only have to worry about the following languages:**

* Clojure
* Haskell
* Java
* JavaScript
* OCaml
* Perl
* PHP
* Python
* Ruby
* Scala
* Scheme
* Tcl

Feel more than free to add others!

### Classifying new snippets

Using your corpus, you should extract features for your classifier. Use whatever classifier engine that works best for you _and that you can explain how it works._

Your initial classifier should be able to take a string containing code and return a guessed language for it. It is recommended you also have a method that returns the snippet's percentage chance for each language in a dict.

### Testing your classifier

The `test/` directory contains code snippets. The file `test.csv` contains a list of the file names in the `test` directory and the language of each snippet. Use this set of snippets to test your classifier. _Do not use the test snippets for training your classifier, obviously._

### Code layout

This project should be laid out in accordance with the project layout from _The Hacker's Guide to Python_. It should have tests for things which can be tested. Your classifier should be able to be run with a small controlled corpus for testing.

Your project should also contain an IPython notebook that demonstrates use of your classifier.

## Hard Mode

In addition to the requirements from **Normal Mode**:

Create a runnable Python file that can classify a snippet in a text file, run like this:

`guess_lang.py code-snippet.txt`

where `guess_lang.py` is whatever you name your program and `code-snippet.txt` is any snippet. Your program should print out the language it thinks the snippet is.

To do this, you will likely want to either pre-parse your corpus and output it as features to load or save out your classifier for later use. Otherwise, you'll have to read your entire corpus every time you run the program. That's acceptable, but slow.

You may want to add some command-line flags to your program. You could allow people to choose the corpus, for example, or to get percentage chances instead of one language. To understand how to write a command-line program with arguments and flags, see the [argparse](https://docs.python.org/3/library/argparse.html) module in the standard library.

## Additional Resources

* [TextBlob](http://textblob.readthedocs.org/en/dev/)
* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)
* [Rosetta Code](http://rosettacode.org/wiki/Rosetta_Code)
* [Working with Text Files](https://opentechschool.github.io/python-data-intro/core/text-files.html)
