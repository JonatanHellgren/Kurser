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
