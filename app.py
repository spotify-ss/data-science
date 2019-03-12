from flask import Flask, render_template

import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import pandas as pd
import numpy as np
from sklearn import preprocessing

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    df = pd.read_csv('SpotifyAudioFeaturesNov2018.csv')
    categories = ['acousticness','danceability','energy','instrumentalness','liveness', 'speechiness','tempo']
    df2 = df[categories]
    x = df2.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df2 = pd.DataFrame(x_scaled, columns=categories)

    values=df2.loc[3].values.flatten().tolist()
    values += values[:1]
    values = np.array(values)
    song1 = df['track_name'][3]

    values2=df2.loc[4].values.flatten().tolist()
    values2 += values[:1]
    values2 = np.array(values)
    song2 = df['track_name'][4]

    data = [go.Scatterpolar(
            r = values,
            theta = categories,
            fill = 'toself',
            name = song1
        ),
        go.Scatterpolar(
            r = values2,
            theta = categories,
            fill = 'toself',
            name = song2)]

    layout = go.Layout(
        polar = dict(
            radialaxis = dict(
                visible = True,
                range = [0, 1]
            )
        ),
        showlegend = True
    )

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(data)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/index.html',
                           ids=ids,
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run()