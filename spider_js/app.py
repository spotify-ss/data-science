import pandas as pd
import numpy as np
from sklearn import preprocessing

# Loading the data
df = pd.read_csv('SpotifyAudioFeaturesNov2018.csv')
# Choosing what columns of data will be used
categories = ['acousticness','danceability','energy',
              'instrumentalness','liveness', 'speechiness',
              'tempo']
df2 = df[categories]

# Normalizing the data
x = df2.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df2 = pd.DataFrame(x_scaled, columns=categories)


# Get song names
song_name1 = str(input('First song: '))
song_name2 = str(input('Second song: '))

# Data
values = df2[df['track_name'] == song_name1]
values2 = df2[df['track_name'] == song_name2]
data = pd.concat([values, values2])



# Writing to JSON

data.to_json('spoopy.json')