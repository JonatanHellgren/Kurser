import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from LinnearClassifiers import Perceptron

data = pd.read_csv('a3_first_sample.tsv', sep='\t', names=['stance', 'text'])
X = data['text']
Y = data['stance']

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,
                                                Y,
                                                test_size=0.2,
                                                random_state=55)


def train_stance_classifier(X, Y):
    pipeline = make_pipeline(TfidfVectorizer(), Perceptron())
    pipeline.fit(X, Y)
    return pipeline


clf_svc = train_stance_classifier(Xtrain, Ytrain)
svc_acc = accuracy_score(Ytest, clf_svc.predict(Xtest))
print(svc_acc)
