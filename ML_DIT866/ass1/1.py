import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# Read the CSV file.
url = 'http://www.cse.chalmers.se/~richajo/dit866/data/CTG.csv'
data = pd.read_csv(url, skiprows=1)

# Select the relevant numerical columns.
selected_cols = ['LB', 'AC', 'FM', 'UC', 'DL', 'DS', 'DP', 'ASTV', 'MSTV', 'ALTV',
                 'MLTV', 'Width', 'Min', 'Max', 'Nmax', 'Nzeros', 'Mode', 'Mean',
                 'Median', 'Variance', 'Tendency', 'NSP']
data = data[selected_cols].dropna()

# Shuffle the dataset.
data_shuffled = data.sample(frac=1.0, random_state=0)

# Split into input part X and output part Y.
X = data_shuffled.drop('NSP', axis=1)

# Map the diagnosis code to a human-readable label.


def to_label(y):
    return [None, 'normal', 'suspect', 'pathologic'][(int(y))]


Y = data_shuffled['NSP'].apply(to_label)

# Partition the data into training and test sets.
Xtrain, Xtest, Ytrain, Ytest = train_test_split(
    X, Y, test_size=0.2, random_state=0)


learning_rates = [0.7, 0.6, 0.5, 0.4, 0.3, 0.1]
n_estimators = [16, 32, 64, 128, 256, 512, 1024]
max_depths = range(2, 9)

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
