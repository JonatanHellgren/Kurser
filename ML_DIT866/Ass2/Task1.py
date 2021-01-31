import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

### Step 1 ###
testData = pd.read_csv("testing.csv")
trainingData = pd.read_csv("training.csv")

Xtest = testData.drop("target", axis=1)
Ytest = testData["target"]
Xtrain = trainingData.drop("target", axis=1)
Ytrain = trainingData["target"]

### step 2 ###
Xtrain_dict = Xtrain.to_dict("records")
Xtest_dict = Xtest.to_dict("records")

dv = DictVectorizer()

Xtrain_encoded = dv.fit_transform(Xtrain_dict)
Xtest_encoded = dv.transform(Xtest_dict)

clf = DecisionTreeClassifier()
score = np.mean(cross_val_score(clf, Xtrain_encoded, Ytrain))
print(score)

### step 3 ###
pipe_dv_dtc = make_pipeline(DictVectorizer(), DecisionTreeClassifier())

pipe_dv_dtc.fit(Xtrain_dict, Ytrain)
pred = pipe_dv_dtc.predict(Xtest_dict)
print(accuracy_score(Ytest, pred))

### Task2 ###
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

deepest = 20

acc_dc = np.zeros([2, deepest])

for it in range(deepest):
    # DecisionTreeClassifier
    clf = DecisionTreeClassifier(max_depth=it + 1)
    clf.fit(Xtrain_encoded, Ytrain)

    Yhat = clf.predict(Xtrain_encoded)
    acc_dc[0][it] = accuracy_score(Ytrain, Yhat)

    Ypred = clf.predict(Xtest_encoded)
    acc_dc[1][it] = accuracy_score(Ytest, Ypred)

plt.plot(range(1, deepest + 1), acc_dc[0])
plt.plot(range(1, deepest + 1), acc_dc[1])
plt.savefig("DecisionTreeClassifier.png")

est_range = [1, 10, 50, 100, 200, 300]
acc_rf = np.zeros([len(est_range) * 2, deepest])

for it in range(deepest):
    for jt, est in zip(range(len(est_range)), est_range):
        # RandomForestClassifier
        clf = RandomForestClassifier(max_depth=it + 1, n_estimators=est, n_jobs=-1)
        clf.fit(Xtrain_encoded, Ytrain)

        Yhat = clf.predict(Xtrain_encoded)
        acc_rf[jt * 2][it] = accuracy_score(Ytrain, Yhat)

        Ypred = clf.predict(Xtest_encoded)
        acc_rf[jt * 2 + 1][it] = accuracy_score(Ytest, Ypred)

# Plotting
f, axs = plt.subplots(2, 3, sharey=True)
for ax, it in zip(axs.reshape(-1), range(len(est_range))):
    ax.plot(range(1, deepest + 1), acc_rf[it * 2])
    ax.plot(range(1, deepest + 1), acc_rf[it * 2 + 1])

plt.savefig("RandomForestClassifier.png")

### Task 3 ###
