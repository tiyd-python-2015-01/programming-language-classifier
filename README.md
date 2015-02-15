All appropriate files are included in the directory "plc".  To have my classifier determine what language a code snippet was written in, do the following:
1.  Copy your code snippet into the file "code_snippet.txt"
2.  run "python guess_lang.py" from the command line.
The program will tell you what language it thinks it is, as well as a percentage of how confident it is in that assessment.


The IPython notebook "Code Classifier.ipynb" demonstrates how the classifier is built and runs it against the test codes found in the "test" directory.  Supplemental functions are found in modules referenced by the imports at the start of the notebook.
An additional IPython notebook "split and test.ipynb" contains a classifier trained on a portion of the Benchmarks game code and tested on the remainder of the code.
