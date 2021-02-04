import numpy as np
import pandas as pd


class knnClassifier:
    # simple init function, stores the value for k and the metric to use to
    # measure the distance
    def __init__(self, k=10, metric="euclidian"):
        self.k = k
        self.metric = metric

    # here in fit we save the data in the obejct at load the metric dunction
    def fit(self, X, y):
        self.X = X.values
        self.y = y.values
        # as of now we have only implemented euclidan distance, but with this
        # code it would be easy to inlude several more by just adding more if-statements
        if self.metric == "euclidian":
            self.criterion_function = euclidian_dist
        else:
            raise Exception(f'Unknown metric: {self.metric}')

    # predict classifies each point by looking at it's k closent neighbors
    def predict(self, df):
        pred = np.empty([len(df), 1])  # here we will store the predictions

        for it in range(len(df)):
            row = df.iloc[
                it, :].values  # take row in data and store it as numpy array
            neigh = get_neighbors(self.criterion_function, row, self.X, self.k)
            classes = self.y[neigh]
            unique, counts = np.unique(classes, return_counts=True)
            pred[it] = unique[np.argmax(counts)]  # majority vote

        self.pred = pred.reshape([1, -1])[0]
        return self.pred  # returning the vector of predictions

    # in score we now only have accuracy, but we could easily add more functions
    def score(self, pred, lab):
        lab = lab.values
        score = accuracy(pred, lab)
        return score


# a simple accuracy function to compute a score for our model
def accuracy(pred, y):
    corr = 0
    for it in range(len(pred)):
        if pred[it] == y[it]:
            corr += 1
    return corr / len(pred)


# function that computes the euclidian distance between to points, to not add
# extra compute time we skip the square root since it will yield in the exact
# same results since the square root is a convex function on positive values
# sqrt(x) < sqrt(y) => x < y if x,y>0
def euclidian_dist(arr1, arr2):
    dist = 0
    for it in range(len(arr1)):
        dist += (arr1[it] - arr2[it])**2
    return dist


# this function camputes all the distances and return the k closest to the input
def get_neighbors(metric, row, X, k):
    distances = np.zeros([1, len(X)])
    for it in range(len(X)):
        distances[0][it] = metric(row, X[it])  # now only calls euclidian_dist
    sorted_distances = np.argsort(distances)
    return sorted_distances[
        0][:k]  # return the index of the k closest observations
