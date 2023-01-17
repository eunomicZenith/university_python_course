import pandas as pd
import numpy as np

data = {'Città': ['Palermo', 'Palermo', 'Palermo', 'Catania', 'Catania', 'Catania'],
        'Anno': [2000, 2001, 2002, 2000, 2001, 2002],
        'Popolazioni': [1.7, 1.88, 1.92, 1.1, 1.24, 1.28],
        }

cityframe = pd.DataFrame(data, columns=['Anno', 'Città', 'Popolazioni'])

cityframe['Debito'] = np.arange(stop=5, start=2, step=0.5)
cityframe['Occidentale'] = cityframe['Città'] == 'Palermo'

# december 15th

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']

users = pd.read_table(r'C:\Users\HarryZ\Desktop\Cor Stellae\Code Archive/users.dat',
                      header=None, names=unames, sep='::', engine='python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings= pd.read_table(r'C:\Users\HarryZ\Desktop\Cor Stellae\Code Archive/ratings.dat',
                       header=None, names=rnames, sep='::', engine='python')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(r'C:\Users\HarryZ\Desktop\Cor Stellae\Code Archive/movies.dat',
                       header=None, names=mnames, sep='::', engine='python', encoding='ISO-8859-1')

data = pd.merge(pd.merge(ratings, users), movies)

mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')

ratings_by_title = data.groupby("title").size()

active_titles = ratings_by_title.index[ratings_by_title >= 250]

mean_ratings = mean_ratings.loc[active_titles]

top_female_ratings = mean_ratings.sort_values('F', ascending=False)

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']

sorted_by_diff = mean_ratings.sort_values('diff', ascending=False)

movies['genre'] = movies.pop('genres').str.split('|')

movies_exploded = movies.explode('genre')

ratings_with_genre = pd.merge(pd.merge(movies_exploded, ratings), users)

ratings_with_genre_by_age = ratings_with_genre.groupby(['genre', 'age'])['rating'].mean().unstack('age')

ratings_with_genre_by_age = ratings_with_genre.pivot_table('rating', index='genre', columns='age', aggfunc='mean')

favorite_18 = ratings_with_genre_by_age.sort_values(18, ascending=False)

print(favorite_18)