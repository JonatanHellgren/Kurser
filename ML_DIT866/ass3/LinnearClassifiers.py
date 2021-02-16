import numpy as np


class LinearClassifiers(object):
    def find_classes(self, Y):
        classes = sorted(set(Y))
        if len(classes) != 2:
            raise Exception("this does not seem to be a 2-class problem")
        self.positive_class = classes[0]
        self.negative_class = classes[1]

    def predict(self, X):
        score = X.dot(self.w)
        out = np.select([scores >= 0.0, scores < 0.0],
                        [self.positive_class, self.negative_class])
        return out


class Perceptron(LinearClassifiers):
    def __init__(self, n_iter=10):
        self.n_iter = n_iter

    def fit(self, X, Y):
        self.find_classes(Y)
        n_features = X.shape[1]
        self.w = np.zeros(n_features)
        for i in range(self.n_iter):
            for x, y in zip(X, Y):
                score = self.w.dot(x)
                if score <= 0 and y == self.positive_class:
                    self.w += x
                elif score >= 0 and y == self.negative_class:
                    self.w -= x
