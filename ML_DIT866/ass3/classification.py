import pandas as pd
from sklearn.model_selection import train_test_split
from LinnearClassifiers import Perceptron
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv('a3_first_sample.tsv', sep='\t', names=['stance', 'text'])
X = data['text']
Y = data['stance']

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,
                                                Y,
                                                test_size=0.2,
                                                random_state=55)

vectorizer = TfidfVectorizer()
clf = Perceptron()
