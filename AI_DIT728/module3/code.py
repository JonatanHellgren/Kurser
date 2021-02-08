import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from knn import knnClassifier  # import our knnClassifier function
from sklearn.model_selection import train_test_split

# training
beijing = pd.read_csv("data/Beijing_labeled.csv")
shenyang = pd.read_csv("data/Shenyang_labeled.csv")

# removing the variable that we want to predict
X = pd.concat([beijing, shenyang]).drop("PM_HIGH", axis=1)
X = X.reset_index().drop('index', axis=1)

# setting predicting variable as PM_HIGH
Y = pd.concat([beijing, shenyang])["PM_HIGH"]
Y = Y.reset_index().drop('index', axis=1)

# train-test splitting the data
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.2)

# testing
guangzhou = pd.read_csv("data/Guangzhou_labeled.csv")
shanghai = pd.read_csv("data/Shanghai_labeled.csv")

# evaluation data
Xeval = pd.concat([guangzhou, shanghai]).drop("PM_HIGH", axis=1)
Xeval = Xeval.reset_index().drop('index', axis=1)
Yeval = pd.concat([guangzhou, shanghai])["PM_HIGH"]
Yeval = Yeval.reset_index().drop('index', axis=1)

# initalizing some things for the loop
max_k = 10
scores = np.zeros([2, max_k])

# here in this loop we will see what value for k acheives the best value on the
# test data. We first fit the model on Xtrain and then compute the score of the
# model on both the train and test data, wich we later will plot
for it in range(max_k):
    knn = knnClassifier(k=it + 1)
    knn.fit(Xtrain, Ytrain)
    scores[0][it] = knn.score(knn.predict(Xtrain), Ytrain)
    scores[1][it] = knn.score(knn.predict(Xtest), Ytest)
    print(it + 1)

# simple plot for the accuracy
plt.plot(range(1, max_k + 1), scores[0])
plt.plot(range(1, max_k + 1), scores[1])
plt.xticks(np.arange(1, max_k, step=2))
plt.show()
# it seems like k=17 results in the best test accuracy

# so now we will try it out on the evalutaion data
knn = knnClassifier(k=17)
knn.fit(Xtrain, Ytrain)
knn.score(knn.predict(Xeval), Yeval)
