import pandas as pd

testData = pd.read_csv("testing.csv")
trainingData = pd.read_csv("training.csv")

Xtest = testData.drop("target", axis=1)
Ytest = testData["target"]
Xtrain = trainingData.drop("target", axis=1)
Ytrain = trainingData["target"]
