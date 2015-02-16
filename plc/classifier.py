from sklearn import metrics


def create_xy(df, test_df, startx, columny):
    x_train = df.loc[:, startx:]
    x_test = test_df.loc[:, startx:]
    y_train = df[columny]
    y_test = test_df[columny]
    return x_train, x_test, y_train, y_test


def run_classifier(clf, x_train, x_test, y_train, y_test):
    clf.fit(x_train, y_train)
    predicted = clf.predict(x_test)
    print(metrics.classification_report(y_test, predicted))
    print(metrics.confusion_matrix(y_test, predicted))
    print(metrics.f1_score(y_test, predicted))

def create_train(df, startx, columny):
    x_train = df.loc[:, startx:]
    y_train = df[columny]
    return x_train, y_train
