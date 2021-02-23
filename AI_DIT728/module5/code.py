import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import precision_score, accuracy_score, recall_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, truncnorm, randint, ttest_ind

# loading the data as global variables
with open('wdbc.pkl', 'rb') as f:
    wdbc = pickle.load(f)

X = wdbc.iloc[:, 2:]
Y = wdbc.malignant

# train test split it
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,
                                                Y,
                                                test_size=0.2,
                                                random_state=1729)


# function to take a quick look at the data
def plot_data():
    features = wdbc.columns[2:]
    for feature in features:
        sns.catplot(x='malignant', y=feature, kind='box', data=wdbc)
        plt.title(feature)
        plt.tight_layout()
        plt.savefig(f'./plots/{feature}.png')
    return None


# defining the class rule_based_classifier, to answer part one of the
# implementation
class rule_based_classifier():
    def __init__(self, metric='accuracy', decisions=[]):
        # here we choose what features we are going to consider when making a
        # classification
        self.decisions = decisions
        # here we get to choose what metric we are going to split the data with
        # to find our decision boundrys
        self.metric = metric

    # function to fit the data
    def fit(self, X, Y):
        # load the metric function
        if self.metric == 'precision':
            self.metric_function = precision_score
        elif self.metric == 'accuracy':
            self.metric_function = accuracy_score
        elif self.metric == 'recall':
            self.metric_function = recall_score
        elif self.metric == 'tpr':
            self.metric_function = true_positive_rate
        else:
            raise Exception(f'Unknown metric: {self.metric}')
        # finds best splits for decision varaibles
        self.boundrys = np.empty(len(self.decisions))
        for it, feature in enumerate(self.decisions):
            self.boundrys[it] = find_split(Xtrain.loc[:, feature].values, Y,
                                           self.metric_function)

    # predict function
    def predict(self, X):
        # start out as malignant and if we find a reason for classifying it as
        # benign we will change it to a 1
        pred = np.zeros([len(X), 1])
        feature_n = X.columns
        for it in range(len(X)):  # for each observation
            if pred[it, 0] == 0:  # only consider it if benign
                for ft, feature in enumerate(self.decisions):
                    # here we checks if the observation has a value above the
                    # boundry we found earlier with fit
                    #ind = np.where(feature == feature_n)[0]
                    if X.iloc[it, :].loc[feature] > self.boundrys[ft]:
                        pred[it, 0] = 1
        return pred


# finds bets split cosidering accuracy, recall or precision
def find_split(X, Y, metric):
    # sor the index so that we can consider every possible split
    sort_ind = X.argsort()
    X_s = X[sort_ind]
    Y_s = Y.values[sort_ind]
    # initalizing the loop for best split
    sz = len(X_s)
    best_score = 0
    split = None
    # loop to find the best split
    for it in range(1, sz - 1):
        # if we where to split here we would get these predictions
        pred = np.concatenate((np.zeros(
            [1, it], dtype='int'), np.ones([1, sz - it], dtype='int')),
                              axis=1)[0]
        # computer the score with the given metric
        score = metric(Y_s, pred)
        # checks if we have a new best score
        if score > best_score:
            # update score
            best_score = score
            # returns the best split, which would be inbetween this point and
            # the previous point
            split = (X_s[it] + X_s[it - 1]) / 2
    return split


def true_positive_rate(y_true, y_pred):
    cf = confusion_matrix(y_true, y_pred)
    return cf[1, 1] / (cf[0, 1] + cf[1, 1])


def first():
    large_size = ['area_0', 'radius_0', 'perimeter_0']
    arbitrary_structure = ['compactness_0', 'concavity_0', 'concave points_0']
    hgh_var_txtre = ['texture_2']
    metrics = ['precision', 'accuracy']
    decisions = []
    best_acc = 0
    best_dec = []
    best_met = []
    decisions.append(hgh_var_txtre[0])
    for ls in large_size:
        decisions.append(ls)
        for arb in arbitrary_structure:
            decisions.append(arb)
            for met in metrics:
                cle = rule_based_classifier(metric=met, decisions=decisions)
                cle.fit(Xtrain, Ytrain)
                pred = cle.predict(Xtrain)
                acc = accuracy_score(Ytrain, pred)
                if acc > best_acc:
                    print('new best')
                    print(decisions)
                    print(acc)
                    print(met)
                    best_acc = acc
                    best_dec = decisions.copy()
                    best_met = met
            decisions.pop()
        decisions.pop()
    print(best_dec)
    cle = rule_based_classifier(metric=best_met, decisions=best_dec)
    cle.fit(Xtrain, Ytrain)
    pred = cle.predict(Xtest)
    accuracy_score(Ytest, pred)
    # get quite different results when training with accuracy and precision,
    # recall however is shit, just predict everything as positive
    print('Rule based classifier')
    print(confusion_matrix(Ytest, pred))
    print(f'Accuracy: {accuracy_score(Ytest, pred)}')


def fit_rfCV():
    model_params = {
        'n_estimators': randint(4, 200),
        'max_depth': randint(2, 9)
    }
    clf_rf = RandomForestClassifier()
    clf = RandomizedSearchCV(clf_rf,
                             model_params,
                             n_iter=100,
                             cv=10,
                             n_jobs=-1,
                             random_state=12)
    clf_best = clf.fit(Xtrain, Ytrain)
    return clf_best


def second():
    clf_rf = fit_rfCV()
    clf_rf.fit(Xtrain, Ytrain)
    pred = clf_rf.predict(Xtest)
    print('Random forrest classifier')
    print(confusion_matrix(Ytest, pred))
    print(f'Accuracy: accuracy_score(Ytest, pred)')


def fit_dtCV():
    best = None
    best_score = 0
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=123)
    for it in range(1, 15):
        clf_dt = tree.DecisionTreeClassifier(max_depth=it)
        score = cross_val_score(clf_dt, Xtrain, Ytrain, cv=cv,
                                n_jobs=-1).mean()
        if score > best_score:
            best = it
            best_score = score
    return tree.DecisionTreeClassifier(max_depth=best)


def third():
    clf_dt = tree.DecisionTreeClassifier(max_depth=3, random_state=123)
    clf_dt.fit(Xtrain, Ytrain)
    pred = clf_dt.predict(Xtest)
    print('Decision tree classifier')
    print(confusion_matrix(Ytest, pred))
    print(f'Accuracy: {accuracy_score(Ytest, pred)}')
    print(tree.export_text(clf_dt))


third()


def main():
    first()
    second()
    third()


if __name__ == "__main__":
    main()
