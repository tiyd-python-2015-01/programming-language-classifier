Programming Language Classifier project.

Daniel K. Newell and Zachary J. Huntington-Meath, The Iron Yard, Durham, Python Cohort 2015.

For our classifier, we decided to use the Bernoulli Naive Bayes Classifier. We
decided to use this Classifier after extensively searching our code base
for features we thought would be beneficial. Initially we chose to use the Gaussian
Bayes Classifier to predict the languages. However, we discovered that adding
more features was decreasing the Gaussian Bayes Classifier's ability to distinguish different
languages correctly. For the Gaussian Bayes Classifier, we used the ratio "frequency of feature : # of words in code" for each example of code. For the Bernoulli Naive Bayes Classifier, if the
feature is present in the code, it returns a 1; if it is not, it returns a 0.


To use our classifier, you can create the Bernoulli Naive Bayes Classifier by running
the Bernoulli_classifier_maker.py file. This will create a pickled version
of the classifier as language_dectector.pkl. Then you can run predict_language.py
followed by a file with code in it, and it will return the top three languages with
percentage possibility that it is that language.
An example would be as follows: python predict_language.py code_snippt.txt


We also made a webscraper for Rosetta Code that will look through a given
page and extract an example of code for each language specified. It will then return a file
with the proper extension in the bench folder located in the training folder.
You can run the webscraper by giving a proper Rosetta Code page URL plus what
you would like the fileset to be named. For example,
python web_scraper.py http://rosettacode.org/wiki/Bitmap bit_map
This would scrape the Bitmap code examples and return files for each language
named bit_map plus their extension.
