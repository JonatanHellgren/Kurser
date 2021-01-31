import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# reading the data
movie_genres = pd.read_csv("movie_genres.csv")
user_reviews = pd.read_csv("user_reviews.csv")
genre_only = movie_genres.iloc[:, 2:]

# select user, for assignment 0,1,2,3,4 is asked for
user_txt = input("Type index of user: ")
user = int(user_txt)
# save the movies the user has rated
ratings = user_reviews.iloc[user, 2:]
rated_movies = np.where(ratings > 0)

# compute average rating for each movie using Baysian update with uniform prior
avg_rating = np.zeros([1, len(movie_genres)])
for it in range(len(movie_genres)):
    nonzero = user_reviews.iloc[:, it + 2] > 0  # only could the nonzero ratings
    rated = user_reviews.loc[nonzero].iloc[:, it + 2]
    avg_rating[0][it] = (sum(rated) + 15) / (len(rated) + 5)

# each score starts as the average
score = avg_rating.copy()

# loop to compute the scores
for jt in rated_movies[0]:
    movie1 = genre_only.iloc[jt, :].values
    rating = ratings[jt] - 2.5  # subtracting 2.5 to make low votes count negativly
    for it in range(len(genre_only)):
        if it not in rated_movies[0]:  # no need to count rade movies
            movie2 = genre_only.iloc[it, :].values
            csn_sim = cosine_similarity(movie1.reshape(1, -1), movie2.reshape(1, -1))
            score[0][it] = score[0][it] + csn_sim * rating

# sort out the top 5 scores
top5 = score.argsort()[0][::-1][:5]

# and printing the titles of them movies
print(movie_genres.iloc[top5].movie_title)
print(score[0][top5])
