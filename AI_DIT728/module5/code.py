import matplotlib.pyplot as plt
import pickle
import pandas as pd
import seaborn as sns

with open('wdbc.pkl', 'rb') as f:
    wdbc = pickle.load(f)


def plot_data():
    features = wdbc.columns[2:]
    features[10]
    for feature in features:
        sns.catplot(x='malignant', y=feature, kind='box', data=wdbc)
        plt.title(feature)
        plt.tight_layout()
        plt.savefig(f'./plots/{feature}.png')
    return None


def main():
    plot_data()


if __name__ == "__main__":
    main()
