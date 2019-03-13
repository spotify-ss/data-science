from flask import Flask, request
from flask.json import jsonify, loads
from sklearn.linear_model import LogisticRegression
from decouple import config
import json
import pandas as pd
import numpy as np

app = Flask(__name__)
SECRET_KEY = config("DATA-SCIENCE-KEY")


@app.route("/api/v1.0/closest/<track_id>/<page_number>", methods=["POST"])
def closest_songs(track_id, page_number):
    """Flask POST method that finds closest songs based on normalized distance.

    URL:
        /api/v1.0/closest/<track_id>/<page_number>
    POST Args:
        songs (str-json): list of song information as dictionaries
            track_id (str)
            acousticness (float)
            danceability (float)
            duration_ms (float)
            energy (float)
            instrumentalness (float)
            liveness (float)
            loudness (float)
            speechiness (float)
            tempo (float)
            valence (float)
            popularity (float)
        mean_values (str-json): dictionary of precomputed aggregate song data
            acousticness (dict): dictionary of values associated with
                acousticness
                mean (float)
                stddev (float)
                index (int)
            danceability (dict): same format as acousticness
            duration_ms (dict): same format as acousticness
            energy (dict): same format as acousticness
            instrumentalness (dict): same format as acousticness
            liveness (dict): same format as acousticness
            loudness (dict): same format as acousticness
            speechiness (dict): same format as acousticness
            tempo (dict): same format as acousticness
            valence (dict): same format as acousticness
            popularity (dict): same format as acousticness
    Args:
        track_id (str): Spotify track id for song to compare others to
        page_number (str-int): page number of tracks to return, based on 100
                tracks per page
    Returns:
        (str-json) JSON dictionary of track ids and corresponding distance to
                song
            '[track_id]': [distance (float)]"""
    vals = request.get_json()
    if vals.get("key") != SECRET_KEY:
        return "ERROR - INCORRECT SECRET KEY"
    df = pd.read_json(json.dumps(vals.get("songs")))
    df.index = df["track_id"]
    df = df[["acousticness",
             "danceability",
             "duration_ms",
             "energy",
             "instrumentalness",
             "liveness",
             "loudness",
             "speechiness",
             "tempo",
             "valence",
             "popularity"]]
    labels = []
    label_values = [
        "acousticness",
        "danceability",
        "duration_ms",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "tempo",
        "valence",
        "popularity"
    ]
    mean_values = vals.get("mean_values")
    for v in label_values:
        df[v] = (df[v] - mean_values[v]["mean"]) / mean_values[v]["stddev"]
        labels.append([v, mean_values[v]["index"]])
    dist = (((df.loc[track_id] - df)**2).sum(axis=1)**0.5).sort_values()
    page_number = int(page_number)
    dist = dist.iloc[100*page_number:min(dist.shape[0], 100*page_number+100)]
    return dist.to_json()


@app.route("/api/v1.0/closest/target/<page_number>", methods=["POST"])
def closest_songs_by_val(page_number):
    """Flask POST method that finds songs close to target based on normalized
            distance.

    URL:
        /api/v1.0/closest/target/<page_number>
    POST Args:
        songs (str-json): list of song information as dictionaries
            track_id (str)
            acousticness (float)
            danceability (float)
            duration_ms (float)
            energy (float)
            instrumentalness (float)
            liveness (float)
            loudness (float)
            speechiness (float)
            tempo (float)
            valence (float)
            popularity (float)
        mean_values (str-json): dictionary of precomputed aggregate song data
            acousticness (dict): dictionary of values associated with
                acousticness
                mean (float)
                stddev (float)
                index (int)
            danceability (dict): same format as acousticness
            duration_ms (dict): same format as acousticness
            energy (dict): same format as acousticness
            instrumentalness (dict): same format as acousticness
            liveness (dict): same format as acousticness
            loudness (dict): same format as acousticness
            speechiness (dict): same format as acousticness
            tempo (dict): same format as acousticness
            valence (dict): same format as acousticness
            popularity (dict): same format as acousticness
        target (str-json): dictionary of target values
            acousticness (float)
            danceability (float)
            duration_ms (float)
            energy (float)
            instrumentalness (float)
            liveness (float)
            loudness (float)
            speechiness (float)
            valence (float)
            popularity (float)
    Args:
        page_number (str-int): page number of tracks to return, based on 100
                tracks per page
    Returns:
        (str-json) JSON dictionary of track ids and corresponding distance to
                song
            '[track_id]': [distance (float)]"""
    vals = request.get_json()
    if vals.get("key") != SECRET_KEY:
        return "ERROR - INCORRECT SECRET KEY"
    df = pd.read_json(json.dumps(vals.get("songs")))
    df.index = df["track_id"]
    df = df[["acousticness",
             "danceability",
             "duration_ms",
             "energy",
             "instrumentalness",
             "liveness",
             "loudness",
             "speechiness",
             "tempo",
             "valence",
             "popularity"]]
    target = pd.read_json(json.dumps(vals.get("target")))
    labels = []
    label_values = [
        "acousticness",
        "danceability",
        "duration_ms",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "tempo",
        "valence",
        "popularity"
    ]
    mean_values = vals.get("mean_values")
    for v in mean_values:
        df[v] = (df[v] - mean_values[v]["mean"]) / mean_values[v]["stddev"]
        target[v] = (target[v] - mean_values[v]["mean"]) / \
            mean_values[v]["stddev"]
        labels.append([v, mean_values[v]["index"]])
    dist = (((target.iloc[0] - df)**2).sum(axis=1)**0.5).sort_values()
    page_number = int(page_number)
    dist = dist.iloc[100*page_number:100*page_number+100]
    return dist.to_json()


@app.route("/api/v1.0/user/fit", methods=["POST"])
def fit_user():
    """Flask POST method that returns logistic model coefficients based on user
            preferences.

    URL:
        /api/v1.0/user/fit
    POST Args:
        pos_songs (str-json): list of user approved song information as
                dictionaries
            track_id (str)
            acousticness (float)
            danceability (float)
            duration_ms (float)
            energy (float)
            instrumentalness (float)
            liveness (float)
            loudness (float)
            speechiness (float)
            tempo (float)
            valence (float)
            popularity (float)
        neg_songs (str-json): list of user disapproved song information as
                dictionaries
            track_id (str)
            acousticness (float)
            danceability (float)
            duration_ms (float)
            energy (float)
            instrumentalness (float)
            liveness (float)
            loudness (float)
            speechiness (float)
            tempo (float)
            valence (float)
            popularity (float)
        mean_values (str-json): dictionary of precomputed aggregate song data
            acousticness (dict): dictionary of values associated with
                acousticness
                mean (float)
                stddev (float)
                index (int)
            danceability (dict): same format as acousticness
            duration_ms (dict): same format as acousticness
            energy (dict): same format as acousticness
            instrumentalness (dict): same format as acousticness
            liveness (dict): same format as acousticness
            loudness (dict): same format as acousticness
            speechiness (dict): same format as acousticness
            tempo (dict): same format as acousticness
            valence (dict): same format as acousticness
            popularity (dict): same format as acousticness
    Args:
        None
    Returns:
        (str-json) JSON dictionary of model coefficients
            acousticness (list): coefficient information for acousticness
                (int) index
                (float) coefficient value
            danceability (list): same as acousticness
            duration_ms (list): same as acousticness
            energy (list): same as acousticness
            instrumentalness (list): same as acousticness
            liveness (list): same as acousticness
            loudness (list): same as acousticness
            speechiness (list): same as acousticness
            tempo (list): same as acousticness
            time_signature (list): same as acousticness
            valence (list): same as acousticness
            intercept (float)"""
    vals = request.get_json()
    if vals.get("key") != SECRET_KEY:
        return "ERROR - INCORRECT SECRET KEY"
    pos_songs = pd.read_json(json.dumps(vals.get("pos_songs")))
    pos_songs["value"] = 1
    neg_songs = pd.read_json(json.dumps(vals.get("neg_songs")))
    neg_songs["value"] = 0
    X = pd.concat([pos_songs, neg_songs])
    Y = X["value"]
    cols = ["acousticness",
            "danceability",
            "duration_ms",
            "energy",
            "instrumentalness",
            "liveness",
            "loudness",
            "speechiness",
            "time_signature",
            "valence",
            "popularity"]
    X = X[cols]
    labels = []
    label_values = [
        "acousticness",
        "danceability",
        "duration_ms",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "tempo",
        "valence",
        "popularity"
    ]
    mean_values = vals.get("mean_values")
    for v in mean_values:
        X[v] = (X[v] - mean_values[v]["mean"]) / mean_values[v]["stddev"]
        labels.append([v, mean_values[v]["index"]])
    log_reg = LogisticRegression(
        random_state=0,
        solver='saga'
    )
    log_reg.fit(X, Y)
    user_coef = {}
    for i in range(len(log_reg.coef_[0])):
        user_coef[labels[i][0]] = [labels[i][1], log_reg.coef_[0][i]]
    user_coef["intercept"] = log_reg.intercept_[0]
    return jsonify(user_coef)


@app.route("/api/v1.0/user/predict/<page_number>", methods=["POST"])
def predict_user(page_number):
    """Flask POST method that finds closest songs based on precomputed logistic
            regression model.

    URL:
        /api/v1.0/closest/<track_id>/<page_number>
    POST Args:
        songs (str-json): list of song information as dictionaries
            track_id (str)
            acousticness (float)
            danceability (float)
            duration_ms (float)
            energy (float)
            instrumentalness (float)
            liveness (float)
            loudness (float)
            speechiness (float)
            tempo (float)
            valence (float)
            popularity (float)
        mean_values (str-json): dictionary of precomputed aggregate song data
            acousticness (dict): dictionary of values associated with
                acousticness
                mean (float)
                stddev (float)
                index (int)
            danceability (dict): same format as acousticness
            duration_ms (dict): same format as acousticness
            energy (dict): same format as acousticness
            instrumentalness (dict): same format as acousticness
            liveness (dict): same format as acousticness
            loudness (dict): same format as acousticness
            speechiness (dict): same format as acousticness
            tempo (dict): same format as acousticness
            valence (dict): same format as acousticness
            popularity (dict): same format as acousticness
        model (str-json):
            acousticness (list): coefficient information for acousticness
                (int) index
                (float) coefficient value
            danceability (list): same as acousticness
            duration_ms (list): same as acousticness
            energy (list): same as acousticness
            instrumentalness (list): same as acousticness
            liveness (list): same as acousticness
            loudness (list): same as acousticness
            speechiness (list): same as acousticness
            tempo (list): same as acousticness
            valence (list): same as acousticness
            popularity (list): same as acousticness
            intercept (float)
    Args:
        page_number (str-int): page number of tracks to return, based on 100
            tracks per page
    Returns:
        (str-json) JSON dictionary of track ids and corresponding distance to
            song
            '[track_id]': [distance (float)]"""
    vals = request.get_json()
    if vals.get("key") != SECRET_KEY:
        return "ERROR - INCORRECT SECRET KEY"
    df = pd.read_json(json.dumps(vals.get("songs")))
    df.index = df["track_id"]
    df = df[["acousticness",
             "danceability",
             "duration_ms",
             "energy",
             "instrumentalness",
             "liveness",
             "loudness",
             "speechiness",
             "tempo",
             "valence",
             "popularity"]]
    mean_values = vals.get("mean_values")
    label_values = [
        "acousticness",
        "danceability",
        "duration_ms",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "tempo",
        "valence",
        "popularity"
    ]
    for v in mean_values:
        df[v] = (df[v] - mean_values[v]["mean"]) / mean_values[v]["stddev"]
    model_vals = request.values.get("model")
    log_reg = LogisticRegression(
        random_state=0,
        solver='saga'
    )
    log_reg.intercept_ = np.array(model_vals["intercept"]).reshape(1,)
    coef = np.zeros((1, len([k for k in model_vals]) - 1))
    for key in model_vals:
        if key != "intercept":
            coef[0, model_vals[key][0]] = model_vals[key][1]
    log_reg.coef_ = coef
    df["prob"] = log_reg.predict_proba(df)[:, 1]
    dist = df["prob"].sort_values(ascending=False)
    page_number = int(page_number)
    dist = dist.iloc[100*page_number:100*page_number+100]
    return dist.to_json()


@app.route("/api/v1.0/aggregate", methods=["POST"])
def aggregate():
    """Flask POST method that creates aggregate values for entire song
            database.

    URL:
        /api/v1.0/aggregate
    POST Args:
        songs (str-json): list of song information as dictionaries
            acousticness (float)
            danceability (float)
            duration_ms (float)
            energy (float)
            instrumentalness (float)
            liveness (float)
            loudness (float)
            speechiness (float)
            tempo (float)
            valence (float)
            popularity (float)
    Args:
        None
    Returns:
        (str-json): dictionary of precomputed aggregate song data
            acousticness (dict): dictionary of values associated with
                    acousticness
                mean (float)
                stddev (float)
                min (float)
                max (float)
                index (int)
            danceability (dict): same format as acousticness
            duration_ms (dict): same format as acousticness
            energy (dict): same format as acousticness
            instrumentalness (dict): same format as acousticness
            liveness (dict): same format as acousticness
            loudness (dict): same format as acousticness
            speechiness (dict): same format as acousticness
            tempo (dict): same format as acousticness
            valence (dict): same format as acousticness
            popularity (dict): same format as acousticness"""
    vals = request.get_json()
    if vals.get("key") != SECRET_KEY:
        return "ERROR - INCORRECT SECRET KEY"
    df = pd.read_json(json.dumps(vals.get("songs")))
    df = df[["acousticness",
             "danceability",
             "duration_ms",
             "energy",
             "instrumentalness",
             "liveness",
             "loudness",
             "speechiness",
             "tempo",
             "valence",
             "popularity"]]
    mean_values = {}
    for i, c in enumerate(list(df)):
        mean_values[c] = {
            "mean": float(df[c].mean()),
            "stddev": float(df[c].std()),
            "min": float(df[c].min()),
            "max": float(df[c].max()),
            "index": i
        }
    return json.dumps(mean_values)
