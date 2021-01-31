import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

learning_rates = [0.7, 0.6, 0.5, 0.4, 0.3, 0.1]
n_estimators = [64, 128, 256, 512, 1024, 2048, 4096]
max_depths = range(2, 5)

best = 0
score = 0

params = [0, 0, 0]
count = 0

# to find the best values we are doing an exhaulstic search
# this takes a while but it is an easy way for finding the best hyper-parameter
# values
for lr in learning_rates:
    for n_est in n_estimators:
        for mx_dp in max_depths:

            # printing out the progress
            print(count/(len(learning_rates)*len(n_estimators)*len(max_depths)))

            # printing
            clf_gb = GradientBoostingClassifier(learning_rate=lr, n_estimators=n_est,
                                                max_depth=mx_dp)
            score = np.mean(cross_val_score(clf_gb, Xtrain, Ytrain, n_jobs=-1))

            if score > best:
                best = score
                params = [lr, n_est, mx_dp]

            count += 1


print(best, params)
