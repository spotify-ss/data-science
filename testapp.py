import random
import json
import csv

import requests
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db')
Base = declarative_base()


class Song(Base):
    __tablename__ = 'songs'
    track_id = Column('track_id', String, primary_key=True, nullable=False)
    artist_name = Column('artist_name', String, nullable=False)
    track_name = Column('track_name', String, nullable=False)
    acousticness = Column('acousticness', Float, nullable=False)
    danceability = Column('danceability', Float, nullable=False)
    duration_ms = Column('duration_ms', Float, nullable=False)
    energy = Column('energy', Float, nullable=False)
    instrumentalness = Column('instrumentalness', Float, nullable=False)
    key = Column('key', Float, nullable=False)
    liveness = Column('liveness', Float, nullable=False)
    loudness = Column('loudness', Float, nullable=False)
    mode = Column('mode', Float, nullable=False)
    speechiness = Column('speechiness', Float, nullable=False)
    tempo = Column('tempo', Float, nullable=False)
    time_signature = Column('time_signature', Float, nullable=False)
    valence = Column('valence', Float, nullable=False)
    popularity = Column('popularity', Float, nullable=False)


Base.metadata.drop_all(engine)

temp_df = pd.read_csv("SpotifyAudioFeaturesNov2018.csv")
temp_df = temp_df.drop_duplicates(subset="track_id")

import_songs = text("""INSERT INTO songs(
        track_id,
        artist_name,
        track_name,
        acousticness,
        danceability,
        duration_ms,
        energy,
        instrumentalness,
        key,
        liveness,
        loudness,
        mode,
        speechiness,
        tempo,
        time_signature,
        valence,
        popularity
    ) VALUES(
        :track_id,
        :artist_name,
        :track_name,
        :acousticness,
        :danceability,
        :duration_ms,
        :energy,
        :instrumentalness,
        :key,
        :liveness,
        :loudness,
        :mode,
        :speechiness,
        :tempo,
        :time_signature,
        :valence,
        :popularity)""")
conn = engine.connect()
temp_df.to_sql('songs', con=engine)
print(list(engine.execute("SELECT COUNT(*) FROM songs")))

Session = sessionmaker(bind=engine)
session = Session()

rows = [u._asdict() for u in session.query(Song).with_entities(
    Song.acousticness,
    Song.danceability,
    Song.duration_ms,
    Song.energy,
    Song.instrumentalness,
    Song.key,
    Song.liveness,
    Song.loudness,
    Song.mode,
    Song.speechiness,
    Song.tempo,
    Song.time_signature,
    Song.valence,
    Song.popularity
).all()]
temp_df = pd.read_json(json.dumps(rows))
mean_values = {}
for i, c in enumerate(list(temp_df)):
    mean_values[c] = {
        "mean": float(temp_df[c].mean()),
        "stddev": float(temp_df[c].std()),
        "min": float(temp_df[c].min()),
        "max": float(temp_df[c].max()),
        "index": i
    }
mean_values = json.dumps(mean_values)


def closest_songs(track_id, page_number):
    data = [u._asdict() for u in session.query(Song).with_entities(
        Song.track_id,
        Song.acousticness,
        Song.danceability,
        Song.duration_ms,
        Song.energy,
        Song.instrumentalness,
        Song.key,
        Song.liveness,
        Song.loudness,
        Song.mode,
        Song.speechiness,
        Song.tempo,
        Song.time_signature,
        Song.valence,
        Song.popularity
    ).all()]
    req = requests.post(
        'http://localhost:5000/api/v1.0/closest/{}/{}'.format(track_id,
                                                              page_number),
        data={
            'songs': json.dumps(data),
            'mean_values': mean_values
        }
    )
    print(req.text)


def closest_songs_by_val(page_number):
    data = [u._asdict() for u in session.query(Song).with_entities(
        Song.track_id,
        Song.acousticness,
        Song.danceability,
        Song.duration_ms,
        Song.energy,
        Song.instrumentalness,
        Song.key,
        Song.liveness,
        Song.loudness,
        Song.mode,
        Song.speechiness,
        Song.tempo,
        Song.time_signature,
        Song.valence,
        Song.popularity
    ).all()]
    target = [{
        "acousticness": random.normalvariate(0.0, 1.0),
        "danceability": random.normalvariate(0.0, 1.0),
        "duration_ms": random.normalvariate(0.0, 1.0),
        "energy": random.normalvariate(0.0, 1.0),
        "instrumentalness": random.normalvariate(0.0, 1.0),
        "key": random.normalvariate(0.0, 1.0),
        "liveness": random.normalvariate(0.0, 1.0),
        "loudness": random.normalvariate(0.0, 1.0),
        "mode": random.normalvariate(0.0, 1.0),
        "speechiness": random.normalvariate(0.0, 1.0),
        "tempo": random.normalvariate(0.0, 1.0),
        "time_signature": random.normalvariate(0.0, 1.0),
        "valence": random.normalvariate(0.0, 1.0),
        "popularity": random.normalvariate(0.0, 1.0)
    }]
    print(target)
    req = requests.post(
        'http://localhost:5000/api/v1.0/closest/{}'.format(page_number),
        data={
            'songs': json.dumps(data),
            'target': json.dumps(target),
            'mean_values': mean_values
        }
    )
    print(req.text)


def fit_user():
    data = [u._asdict() for u in session.query(Song).with_entities(
        Song.acousticness,
        Song.danceability,
        Song.duration_ms,
        Song.energy,
        Song.instrumentalness,
        Song.key,
        Song.liveness,
        Song.loudness,
        Song.mode,
        Song.speechiness,
        Song.tempo,
        Song.time_signature,
        Song.valence,
        Song.popularity
    ).all()]
    data = random.sample(data, k=70)
    data = {
        "pos_songs": json.dumps(data[:40]),
        "neg_songs": json.dumps(data[40:]),
        'mean_values': mean_values
    }
    req = requests.post(
        'http://localhost:5000/api/v1.0/user/fit',
        data=data
    )
    print(req.text)


def predict_user(page_number):
    data = [u._asdict() for u in session.query(Song).with_entities(
        Song.track_id,
        Song.acousticness,
        Song.danceability,
        Song.duration_ms,
        Song.energy,
        Song.instrumentalness,
        Song.key,
        Song.liveness,
        Song.loudness,
        Song.mode,
        Song.speechiness,
        Song.tempo,
        Song.time_signature,
        Song.valence,
        Song.popularity
    ).all()]
    model = {
        "acousticness": [0, random.normalvariate(0.0, 1.0)],
        "danceability": [1, random.normalvariate(0.0, 1.0)],
        "duration_ms": [2, random.normalvariate(0.0, 1.0)],
        "energy": [3, random.normalvariate(0.0, 1.0)],
        "instrumentalness": [4, random.normalvariate(0.0, 1.0)],
        "key": [5, random.normalvariate(0.0, 1.0)],
        "liveness": [6, random.normalvariate(0.0, 1.0)],
        "loudness": [7, random.normalvariate(0.0, 1.0)],
        "mode": [8, random.normalvariate(0.0, 1.0)],
        "speechiness": [9, random.normalvariate(0.0, 1.0)],
        "tempo": [10, random.normalvariate(0.0, 1.0)],
        "time_signature": [11, random.normalvariate(0.0, 1.0)],
        "valence": [12, random.normalvariate(0.0, 1.0)],
        "popularity": [13, random.normalvariate(0.0, 1.0)],
        "intercept": random.normalvariate(0.0, 1.0)
    }
    print(model)
    req = requests.post(
        'http://localhost:5000/api/v1.0/user/predict/{}'.format(page_number),
        data={
            'songs': json.dumps(data),
            'mean_values': mean_values,
            'model': json.dumps(model)
        }
    )
    print(req.text)


if __name__ == "__main__":
    closest_songs("049RxG2laEl9U1PGYeIqLV", 0)
    closest_songs_by_val(0)
    fit_user()
    predict_user(0)
