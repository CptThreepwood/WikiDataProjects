import math

import pandas
import numpy as np
import matplotlib.pyplot as plt

N_GENRES = 10

genre_data = pandas.read_csv('AlbumCountByYearAndGenre.csv')

## Drop years manually (so that I have a nice continuous plot)
allowed_years = [year for year in range(1940, 2021, 1)]
year_totals = genre_data.groupby('year').sum()['albumCount']
allowed_year_rows = genre_data['year'].apply(lambda year: year in allowed_years)

genre_totals = genre_data.groupby('genreLabel').sum()['albumCount']
allowed_genres = genre_totals.sort_values(ascending=False).index[:N_GENRES]
allowed_genre_rows = genre_data['genreLabel'].apply(lambda x: x in allowed_genres)

filtered_genres = genre_data.loc[
    allowed_year_rows & allowed_genre_rows
].reset_index(drop=True).set_index(['genreLabel', 'year'])

## Sort genres

def indicative_year(genre):
    ## Year the genre had its most albums
    return filtered_genres.loc[genre].idxmax()[0]

    ## First year that the genre had an album
    #return min(filtered_genres.loc[genre].index)

sorted_genres = sorted(allowed_genres, key=lambda genre: indicative_year(genre))

## Make plot
reshaped_dataset = np.array([
    np.array([
        (
            filtered_genres.loc[(genre, year), 'albumCount']
            if (genre, year) in filtered_genres.index else 0
        ) for year in allowed_years
    ]) for genre in sorted_genres
])

x_width = math.ceil(np.max(reshaped_dataset)/100) * 100
x_locations = [
    i*x_width + (x_width/2)
    for i in range(len(sorted_genres))
]

fig, ax = plt.subplots(figsize=(15,10))

for x_loc, genre in zip(x_locations, reshaped_dataset):
    lefts = x_loc - 0.5 * genre
    ax.barh(allowed_years, genre, height=1, left=lefts, align='center')

ax.set_xlim([0, max(x_locations) + x_width/2])
ax.set_xticks(x_locations)
ax.set_xticklabels(sorted_genres, rotation=90, ha='center')

ax.invert_yaxis()

ax.set_ylabel("Year")
ax.set_xlabel("Genre")

plt.tight_layout()

fig.savefig('Absolute.jpg', dpi=300)
