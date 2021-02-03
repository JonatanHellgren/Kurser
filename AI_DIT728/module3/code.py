import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn import datasets

# training
beijing = pd.read_csv("data/Beijing_labeled.csv")
shenyang = pd.read_csv("data/Shenyang_labeled.csv")

Xtrain = pd.concat([beijing, shenyang]).drop("PM_HIGH", axis=1)
Xtrain = Xtrain.reset_index().drop('index', axis=1)

Ytrain = pd.concat([beijing, shenyang])["PM_HIGH"]
Ytain = Ytrain.reset_index().drop('index', axis=1)

# testing
guangzhou = pd.read_csv("data/Guangzhou_labeled.csv")
shanghai = pd.read_csv("data/Shanghai_labeled.csv")

Xtest = pd.concat([guangzhou, shanghai]).drop("PM_HIGH", axis=1)
Xtest = Xtest.reset_index().drop('index', axis=1)
Ytest = pd.concat([guangzhou, shanghai])["PM_HIGH"]
Ytest = Ytest.reset_index().drop('index', axis=1)

knn = knnClassifier()
knn.fit(Xtrain, Ytrain)
knn.predict(Xtest)
knn.score(knn.predict(Xtest), Ytest)

iris = datasets.load_iris()

X = iris.data[:, :2]
y = iris.target

classifier = knnClassifier()
classifier.fit(X, y)

X1, X2 = np.meshgrid(
    np.arange(start=X[:, 0].min() - 1, stop=X[:, 0].max() + 1, step=0.01),
    np.arange(start=X[:, 1].min() - 1, stop=X[:, 1].max() + 1, step=0.01))
plt.contourf(X1,
             X2,
             classifier.predict(np.array([X1.ravel(),
                                          X2.ravel()]).T).reshape(X1.shape),
             alpha=0.75)
plt.scatter(X[:, 0], X[:, 1], c=y)

plt.savefig('normal_knn.png')
