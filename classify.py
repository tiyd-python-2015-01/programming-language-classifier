import pickle
import os
import os.path
import pandas as pd
import nltk
import re
import numpy as np
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
import lang_orig as lg

def read_test_data():
    files = lg.read_files("./test")
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

def select_features_new_test(word_list, final):
        final_list = {}
        #exclude_list = ['l','6','d','x1','x2','5','j','m','w','i','e','g','4','v','n','0','1','a','x','n','y','b','2','c','s','3']
        for key in final:
            found = 0
            for word, score in word_list:
        #        if word not in exclude_list:
                if word == key:
                        found = score
                        break
            final_list[key] = round(found,5)
        return final_list

#def test_new_models(data, final_words, clf):
#    new_target = data['Language'].values
#    token_blob = return_tokenized_data(data)
#    word_list = calculate_scores(token_blob)
#    final = select_features_new_test(word_list, final_words)
#    print('newmodelx word list',final)
#    new_x =  create_vectors(final,data)
#    print('nwx',new_x)
#    predicted = clf.predict(new_x)
#    for pp in range(len(predicted)):
#        print('predicted',predicted[pp],new_target[pp])
#    scores = cross_val_score(clf, new_x, new_target, cv=2)
#    print(metrics.confusion_matrix(new_target, predicted))
#    print(metrics.classification_report(new_target, predicted))
    #print(metrics.f1_score(new_target, predicted))

def setup_data():
    cls = pickle.load( open( "model.p", "rb" ) )
    final_features = pickle.load( open( "features.p", "rb" ) )
    return final_features, cls

def return_tokens(code):
    tokens = nltk.word_tokenize(code)
    return tb(' '.join(tokens))

def create_vectors_new_test(features):
    vec = DictVectorizer()
    return vec.fit_transform(features).toarray()

def predict(code, model, final_features):
    token_blob = return_tokens(code)
    word_list = lg.calculate_scores(token_blob)
    features = select_features_new_test(word_list, final_features)
    #print('newmodelx word list',final)
    #print(features)
    new_x = create_vectors_new_test(features)
    #print('nwx',new_x)
    predicted = model.predict(new_x)
    predicted_probs = model.predict_proba(new_x)
    return predicted, predicted_probs

def print_probabilities(probas, model):
    for ind in range(len(probas[0])):
        print(model.classes_[ind],':',probas[0][ind])


def test_all_new_files(test_data, model, final_features):
    agreement = 0
    total = 0
    for ind, row in test_data.iterrows():

        predicted, probas = predict(row['Code'], model, final_features)
        print("I predicted: {}. It was: {}".format(predicted[0], row['Language']))
        #print_probabilities(probas, model)
        total +=1
        if predicted[0].lower() == row['Language'].lower():
            agreement +=1
    print("Success Rate of Classification:",round(agreement*100/total,2))

test_data = read_test_data()
model_features, model = setup_data()
test_all_new_files(test_data, model, model_features)
