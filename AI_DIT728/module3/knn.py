import numpy as np
from math import sqrt


class knnClassifier:
    def __init__(self, k=10, metric="euclidian"):
        self.k = k
        self.metric = metric

    def fit(self, X, y):
        self.X = X.values
        self.y = y
        if self.metric == "euclidian":
            self.criterion_function = euclidian_dist
        else:
            raise Exception(f'Unknown metric: {self.metric}')

    def predict(self, df):
        mat = df.values
        pred = np.empty([len(mat), 1])
        for row, it in zip(mat, range(len(mat))):
            neigh = get_neighbors(self.criterion_function, row, self.X, self.k)
            classes = self.y[neigh]
            unique, counts = np.unique(classes, return_counts=True)
            pred[it] = unique[np.argmax(counts)]
        self.pred = pred.reshape([1, -1])[0]
        return self.pred

    def score(self, pred, lab):
        score = accuracy(pred, lab)
        return score


def accuracy(pred, y):
    corr = 0
    for it in range(len(pred)):
        if pred[it] == y[it]:
            corr += 1
    return corr / len(pred)


def euclidian_dist(arr1, arr2):
    dist = 0
    for it in range(len(arr1)):
        dist += (arr1[it] - arr2[it])**2
    return dist


def get_neighbors(metric, row, X, k):
    distances = np.zeros([1, len(X)])
    for it in range(len(X)):
        distances[0][it] = metric(row, X[it])
    sorted_distances = np.argsort(distances)
    return sorted_distances[0][:k]
