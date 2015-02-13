import os
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
import os.path
import pandas as pd
import csv
import nltk
from textblob import TextBlob as tb
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import BernoulliNB

from sklearn.feature_extraction.text import CountVectorizer

def read_train_files():
    file_list = []
    for root, dirs, files in os.walk("./train/bench"):
        for name in files:
            file_list.append(os.path.join(root, name))
        for name in dirs:
            file_list.append((os.path.join(root, name)))
    return file_list

def all_extensions(file_list):
    return set([os.path.splitext(file)[1] for file in file_list])

def get_extension(file):
    return os.path.splitext(file)[1]

def get_language(ext):
    if ext in ['.clj', '.cljs', '.edn', '.clojure']:
        return 'Clojure'
    elif ext in ['.hs', '.lhs','ghc']:
        return 'Haskell'
    elif ext in ['.java', '.class', '.jar']:
        return 'Java'
    elif ext in ['.js', '.javascript']:
        return 'Javascript'
    elif ext in ['.pl', '.pm', '.t', '.pod','.perl']:
        return 'Perl'
    elif ext in ['.php', '.phtml', '.php4', '.php3', '.php5', '.phps']:
        return 'PHP'
    elif ext in ['.ocaml','.ml']:
        return 'Ocaml'
    elif ext in ['.py', '.pyw', '.pyc', '.pyo', '.pyd', '.python3']:
        return "Python"
    elif ext in ['.rb', '.rbw', '.jruby']:
        return "Ruby"
    elif ext in ['.scala']:
        return 'Scala'
    elif ext in ['.scm', '.ss','.racket']:
        return "Scheme"
    elif ext in ['.tcl']:
        return "Tcl"
    return None

def read_train_data():
    files = read_train_files()
    main_list=[]
    for file in files:
        ext = get_extension(file)
        lang = get_language(ext)
        if lang != None:
            file_lang = []
            with open(file,errors="surrogateescape") as in_file:
                texto = in_file.read()
            main_list.append([texto,lang])
    return main_list

def join_all_code(content):
    all_code = []
    for ind, row in content.iterrows():
        all_code.append(row['Code'])
    return ''.join(all_code)

def tokenize(content):
    return nltk.word_tokenize(content)

def word_freq(word, code):
    if len(code.words) == 0:
        return 0
    else:
        return code.word_counts[word] / len(code.words)

def print_word_score(sorted_list):
    i=0
    for word, score in sorted_list:
        print(word,score)
        i+=1
        if i == 10:
            break

docu = read_train_data()
datadf = pd.DataFrame(docu, columns = ['Code', 'Language'])
#print(datadf.head())
#print(datadf.shape)
#print(datadf['Language'].value_counts())
all_code = join_all_code(datadf)
tokens = tokenize(all_code)
all_tokens = ' '.join(tokens)
token_blob = tb(all_tokens)
scores = {word: word_freq(word,token_blob) for word in token_blob.words}
sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print_word_score(sorted_words)

exclude_list = ['i','n','0','1','a']
#Interesting find: the words "from",'m','on' should not be excluded. Performance lowers"
final = {}
for word, score in sorted_words:
       if score > 0.001 and word not in exclude_list:
           final[word] = round(score,5)

super_final = []

for ind, row in datadf.iterrows():
        mydict = {}
        for word, score in final.items():
            if row['Code'].find(word) != -1:
                mydict[word] = score
        super_final.append(mydict)

from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
new_x = vec.fit_transform(super_final).toarray()
new_x

x_train, x_test, y_train, y_test = train_test_split(new_x, datadf['Language'].values, test_size=0.4, random_state=0)
clf = BernoulliNB()
clf = clf.fit(x_train, y_train)
predicted = clf.predict(x_test)
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))
print(metrics.f1_score(y_test, predicted))
scores = cross_val_score(clf, new_x,datadf['Language'].values, cv=5)
