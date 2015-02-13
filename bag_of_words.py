from make_corpus import get_corpus
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.pipeline import Pipeline
from textblob import TextBlob


df = get_corpus("training/benchmarks/benchmarksgame/bench/")


df['split text'] = df.text.apply(lambda x: x.split())


vector_data = df[['split text']]





vectorizer = CountVectorizer(tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             max_features = 5000)



bow_transformer = CountVectorizer(lambda x: TextBlob(x).words).fit(df['Text'])
messages_bow = bow_transformer.transform(df['Text'])
tfidf_transformer = TfidfTransformer().fit(messages_bow)
messages_tfidf = tfidf_transformer.transform(messages_bow)
attributes_train, attributes_test, class_train, class_test = \
train_test_split(messages_tfidf.toarray(), languages, test_size=0.4, random_state=0)
