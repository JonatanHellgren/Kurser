import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegression

### Step 1 ###
# Imporing the data from .csv file
test = pd.read_csv('testing.csv')
train = pd.read_csv('training.csv')

# Renaming and spliting up into Y and X
Ytrain = train['target']
Ytest = test['target']
Xtrain = train.drop('target', axis=1)
Xtest = test.drop('target', axis=1)

Xtrain['age'] = pd.to_numeric(Xtrain['age'])
### Step 2 ###
# transform Xtrain into dictonary
dict_Xtrain = Xtrain.to_dict('records')

# create a dictonary vectorizer function and fitting it on Xtrain
dv = DictVectorizer()

# fit and trasforming Xtrain
Xtrain_encoded = dv.fit_transform(dict_Xtrain)

# transforming Xtest
Xtest_encoded = dv.transform(Xtest.to_dict('records'))

# we will try the data on a decision tree classifier with standard settings
clf = LogisticRegression()  # DecisionTreeClassifier()
print(Xtrain.dtypes)
#cross_validate(clf, Xtrain, Ytrain, scoring='accuracy')

### Step 3 ###
