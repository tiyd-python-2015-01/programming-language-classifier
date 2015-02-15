import os
import os.path
import pandas as pd
import nltk
import re
from textblob import TextBlob as tb
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree


def read_files(dir_path):
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            file_list.append(os.path.join(root, name))
        for name in dirs:
            file_list.append((os.path.join(root, name)))
    return file_list


def get_extension(file):
    return os.path.splitext(file)[1]


def get_language(ext):
    if ext in ['.clj', '.cljs', '.edn', '.clojure']:
        return 'Clojure'
    elif ext in ['.hs', '.lhs', 'ghc']:
        return 'Haskell'
    elif ext in ['.java', '.class', '.jar']:
        return 'Java'
    elif ext in ['.js', '.javascript']:
        return 'Javascript'
    elif ext in ['.pl', '.pm', '.t', '.pod', '.perl']:
        return 'Perl'
    elif ext in ['.php', '.phtml', '.php4', '.php3', '.php5', '.phps']:
        return 'PHP'
    elif ext in ['.ocaml', '.ml']:
        return 'Ocaml'
    elif ext in ['.py', '.pyw', '.pyc', '.pyo', '.pyd', '.python3']:
        return "Python"
    elif ext in ['.rb', '.rbw', '.jruby']:
        return "Ruby"
    elif ext in ['.scala']:
        return 'Scala'
    elif ext in ['.scm', '.ss', '.racket']:
        return "Scheme"
    elif ext in ['.tcl']:
        return "Tcl"
    return None

def read_train_data():
    files = read_files("./rosetta")
    main_list = []
    for file in files:
        ext = get_extension(file)
        lang = get_language(ext)
        if lang != None:
            file_lang = []
            with open(file, errors="surrogateescape") as in_file:
                texto = in_file.read()
            main_list.append([texto, lang])
    datadf = pd.DataFrame(main_list, columns = ['Code', 'Language'])
    return datadf

def read_test_data():
    files = read_files("./test")
    main_list = []
    for file in files:
            with open(file, errors="surrogateescape") as in_file:
                texto = in_file.read()
            file_name = re.findall(r'\d+', file)
            main_list.append([texto,file_name[0]])
    file_content = pd.DataFrame(main_list, columns=['Code', 'Filename'])
    file_info = pd.read_csv('./test.csv', dtype={'Filename': str, 'Language': str})
    datadf = pd.merge(file_info, file_content, on=['Filename'])
    del datadf['Filename']
    return datadf

def join_all_code(content):
    all_content = [row["Code"] for ind, row in content.iterrows()]
    return ' '.join(all_content)


def tokenize(content):
    tokens = nltk.word_tokenize(content)
    return ' '.join(tokens)


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

def return_tokenized_data(datadf):
    all_code = join_all_code(datadf)
    all_tokens = tokenize(all_code)
    return tb(all_tokens)


def calculate_scores(token_blob):
    scores = {word: word_freq(word,token_blob) for word in token_blob.words}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def select_features(word_list):
    exclude_list = ['i','n','0','1','a']
    final = {}
    counter = 0
    for word, score in word_list:
        if word not in exclude_list:
           final[word] = round(score,5)
        counter += 1
        if counter == 200:
            break
    print("features#", len(final))
    return final

def select_features_new_test(word_list, final):
    final_list = {}
    for key in final:
        found = 0
        for word, score in word_list:
            if word == key:
                found = score
                break
        final_list[key] = round(found,5)
    return final_list


def create_vectors(final,data):
    super_final = []
    for ind, row in data.iterrows():
        mydict = {}
        for word, score in final.items():
            if row['Code'].find(word) != -1:
                mydict[word] = score
            else:
                mydict[word] = 0
        super_final.append(mydict)
    vec = DictVectorizer()
    return vec.fit_transform(super_final).toarray()

def test_model(x,y,model):
    if model == 'tree':
        clf = tree.DecisionTreeClassifier()
    elif model == 'bernoulli':
        clf = BernoulliNB()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)
    clf = clf.fit(x_train, y_train)
    predicted = clf.predict(x_test)
    print('predicted',predicted)
    print(metrics.classification_report(y_test, predicted))
    print(metrics.f1_score(y_test, predicted))
    scores = cross_val_score(clf, x, y, cv=5)
    return scores, clf


def test_new_models(data, final_words, clf):
    new_target = data['Language'].values
    token_blob = return_tokenized_data(data)
    word_list = calculate_scores(token_blob)
    final = select_features_new_test(word_list, final_words)
    new_x =  create_vectors(final,data)
    predicted = clf.predict(new_x)
    for pp in range(len(predicted)):
        print('predicted',predicted[pp],new_target[pp])


def test_model(x,y,model):
    if model == 'tree':
        clf = tree.DecisionTreeClassifier()
    elif model == 'bernoulli':
        clf = BernoulliNB()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)
    clf = clf.fit(x_train, y_train)
    predicted = clf.predict(x_test)
    print('predicted',predicted)
    print(metrics.classification_report(y_test, predicted))
    print(metrics.f1_score(y_test, predicted))
    scores = cross_val_score(clf, x, y, cv=5)
    return scores, clf


if __name__ == '__main__':
    datadf = read_train_data()
    target = datadf['Language'].values
    print(datadf.groupby('Language').count())
    read_test_data()
    token_blob = return_tokenized_data(datadf)
    word_list = calculate_scores(token_blob)
    final_words = select_features(word_list)
    new_x = create_vectors(final_words,datadf)
    bernoulli_score = test_model(new_x, target, 'bernoulli')
    tree_score, clf_model = test_model(new_x, target, 'tree')
    test_data = read_test_data()
    test_new_models(test_data, final_words, clf_model)
