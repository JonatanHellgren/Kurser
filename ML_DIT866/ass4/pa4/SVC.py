import numpy as np
import random
from aml_perceptron import LinearClassifier


class SVC(LinearClassifier):
    """
    An implementation of the SVC learning algorithm
    """
    def __init__(self, instances=10):
        self.instances = instances

    def fit(self, X, Y):
        self.loss_function = hinge_loss
        self.lmbda = 1 / (X.shape[0] * self.instances)

        pegasos(self, X, Y)


def hinge_loss(score, eta, y, x):
    if y * score <= 0:
        return (eta * y) * x
    else:
        return 0


class LogisticRegression(LinearClassifier):
    """
    An implementation of the LogisticRegression learning algorithm, using the
    pegasos algorithm to compute the weights
    """
    def __init__(self, instances=10):
        self.instances = instances

    def fit(self, X, Y):
        self.loss_function = log_loss
        self.lmbda = 1 / (X.shape[0] * self.instances)

        pegasos(self, X, Y)


def log_loss(score, eta, y, x):
    return eta * y * x / (1 + np.exp(y * score))


def pegasos(self, X, Y):
    """
    Train the classifier using the pegasos algorithm
    """

    self.find_classes(Y)

    Ye = self.encode_outputs(Y)

    if not isinstance(X, np.ndarray):
        X = X.toarray()

    n_features = X.shape[1]
    self.w = np.zeros(n_features)

    n_obs = len(Y)

    for it in range(n_obs * 10):

        ind = random.randint(0, n_obs - 1)
        x = X[ind]
        y = Ye[ind]

        eta = 1 / (self.lmbda * (it + 1))

        score = x.dot(self.w)

        self.w = (1 - eta * self.lmbda) * self.w

        self.w += self.loss_function(score, eta, y, x)
