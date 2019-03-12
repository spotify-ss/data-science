# Flask App for Data Science Back-End of Spotify-SS Project

## Available paths

| Method | Path | Description |
| ------------- | ------------- | ------------- |
| `POST` | [`/api/v1.0/closest/<track-id>/<page-number>`](#Closest-(song)) | Get similar songs to specified song. |
| `POST` | [`/api/v1.0/closest/target/<page-number>`](#Closest-(values)) | Get similar songs to input values. |
| `POST` | [`/api/v1.0/user/fit`](#User-(fit)) | Return model values based on user preferences. |
| `POST` | [`/api/v1.0/user/predict/<page-number>`](#User-(predict)) | Return songs based on input user model. |
| `POST` | [`/api/v1.0/aggregate`](#Aggregate) | Return aggregate values for all songs. |

## Closest (song)

__URL:__ `/api/v1.0/closest/<track-id>/<page-number>`

__Method:__ `POST`

__Auth Required:__ NO

__Data Contraints:__

```
<track-id>: [Spotify ID of track to compare to]

<page-number>: [page number to get]

{
    "songs": [
        {
            "track_id": "[valid Spotify track ID]",
            "acousticness": [float value],
            "danceability": [float value],
            "duration_ms": [float value],
            "energy": [float value],
            "instrumentalness": [float value],
            "key": [float value],
            "liveness": [float value],
            "loudness": [float value],
            "mode": [float value],
            "speechiness": [float value],
            "tempo": [float value],
            "time_signature": [float value],
            "valence": [float value],
            "popularity": [float value]
        },
        ...
    ],
    "mean_values": {
        "acousticness": {
            "mean": [mean acousticness float value for all tracks],
            "stddev": [mean acousticness float value for all tracks],
            "index": [column index integer value],
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    }
}
```

__Data Example:__

```
<track-id>: 2RM4jf1Xa9zPgMGRDiht8O

<page-number>: 0

{
    "songs": [
        {
            "track_id": "049RxG2laEl9U1PGYeIqLV",
            "acousticness": 8.11e-05,
            "danceability": 0.813,
            "duration_ms": 132742,
            "energy": 0.731,
            "instrumentalness": 0.91,
            "key": 11,
            "liveness": 0.0727,
            "loudness": -8.932,
            "mode": 1,
            "speechiness": 0.0697,
            "tempo": 124.031,
            "time_signature": 4,
            "valence": 0.944,
            "popularity": 7
        },
        ...
    ],
    "mean_values": {
        "acousticness": {
            "mean": 0.335554970038122,
            "stddev": 0.3430978160761376,
            "index": 0,
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    }
}
```

__Success Response:__

- __Code:__ 200 Ok
- __Content Example:__
    ```
    {
        "[track-id]": [distance from song as float value],
        ...
    }
    ```
- __Notes:__
  - Returns 100 tracks per page.

## Closest (values)

__URL:__ `/api/v1.0/closest/target/<page-number>`

__Method:__ `POST`

__Auth Required:__ NO

__Data Contraints:__

```
<page-number>: [page number to get]

{
    "songs": [
        {
            "track_id": "[valid Spotify track ID]",
            "acousticness": [float value],
            "danceability": [float value],
            "duration_ms": [float value],
            "energy": [float value],
            "instrumentalness": [float value],
            "key": [float value],
            "liveness": [float value],
            "loudness": [float value],
            "mode": [float value],
            "speechiness": [float value],
            "tempo": [float value],
            "time_signature": [float value],
            "valence": [float value],
            "popularity": [float value]
        }
    ],
    "mean_values": {
        "acousticness": {
            "mean": [mean acousticness float value for all tracks],
            "stddev": [mean acousticness float value for all tracks],
            "index": [column index integer value],
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    },
    "target": {
        "acousticness": [target acousticness float value],
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    }
}
```

__Data Example:__

```
<page-number>: 0

{

    "songs": [
        {
            "track_id": "049RxG2laEl9U1PGYeIqLV",
            "acousticness": 8.11e-05,
            "danceability": 0.813,
            "duration_ms": 132742,
            "energy": 0.731,
            "instrumentalness": 0.91,
            "key": 11,
            "liveness": 0.0727,
            "loudness": -8.932,
            "mode": 1,
            "speechiness": 0.0697,
            "tempo": 124.031,
            "time_signature": 4,
            "valence": 0.944,
            "popularity": 7
        },
        ...
    ],
    "mean_values": {
        "acousticness": {
            "mean": 0.335554970038122,
            "stddev": 0.3430978160761376,
            "index": 0,
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    },
    "target": {
        "acousticness": 0.45,
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    }
}
```

__Success Response:__

- __Code:__ 200 Ok
- __Content Example:__
    ```
    {
        "[track-id]": [distance from song as float value],
        ...
    }
    ```
- __Notes:__
  - Returns 100 tracks per page.

## User (fit)

__URL:__ `/api/v1.0/user/fit`

__Method:__ `POST`

__Auth Required:__ NO

__Data Contraints:__

```
{
    "pos_songs": [
        {
            "acousticness": [float value],
            "danceability": [float value],
            "duration_ms": [float value],
            "energy": [float value],
            "instrumentalness": [float value],
            "key": [float value],
            "liveness": [float value],
            "loudness": [float value],
            "mode": [float value],
            "speechiness": [float value],
            "tempo": [float value],
            "time_signature": [float value],
            "valence": [float value],
            "popularity": [float value]
        },
        ...
    ],
    "neg_songs": [
        {
            "acousticness": [float value],
            "danceability": [float value],
            "duration_ms": [float value],
            "energy": [float value],
            "instrumentalness": [float value],
            "key": [float value],
            "liveness": [float value],
            "loudness": [float value],
            "mode": [float value],
            "speechiness": [float value],
            "tempo": [float value],
            "time_signature": [float value],
            "valence": [float value],
            "popularity": [float value]
        },
        ...
    ],
    "mean_values": {
        "acousticness": {
            "mean": [mean acousticness float value for all tracks],
            "stddev": [mean acousticness float value for all tracks],
            "index": [column index integer value],
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    }
}
```

- Notes:
  - pos_songs refer to tracks that the user have approved of, neg_songs refer
    to tracks the user has disapproved of.

__Data Example:__

```
{
    "pos_songs": [
        {
            "acousticness": 8.11e-05,
            "danceability": 0.813,
            "duration_ms": 132742,
            "energy": 0.731,
            "instrumentalness": 0.91,
            "key": 11,
            "liveness": 0.0727,
            "loudness": -8.932,
            "mode": 1,
            "speechiness": 0.0697,
            "tempo": 124.031,
            "time_signature": 4,
            "valence": 0.944,
            "popularity": 7
        },
        ...
    ],
    "neg_songs": [
        {
            "acousticness": 0.0244,
            "danceability": 0.846,
            "duration_ms": 214800,
            "energy": 0.557,
            "instrumentalness": 0.0,
            "key": 8,
            "liveness": 0.286,
            "loudness": -7.259,
            "mode": 1,
            "speechiness": 0.457,
            "tempo": 159.009,
            "time_signature": 4,
            "valence": 0.371,
            "popularity": 10
        },
        ...
    ],
    "mean_values": {
        "acousticness": {
            "mean": 0.335554970038122,
            "stddev": 0.3430978160761376,
            "index": 0,
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    }
}
```

__Success Response:__

- __Code:__ 200 Ok
- __Content Example:__
    ```
    {
        "acousticness": [
            [coefficient index integer value],
            [coefficient float value]
        ],
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...,
        "intercept": [intercept float value]
    }
    ```

## User (predict)

__URL:__ `/api/v1.0/user/predict/<page-number>`

__Method:__ `POST`

__Auth Required:__ NO

__Data Contraints:__

```
<page-number>: 0

{
    "songs": [
        {
            "track_id": "[valid Spotify track ID]",
            "acousticness": [float value],
            "danceability": [float value],
            "duration_ms": [float value],
            "energy": [float value],
            "instrumentalness": [float value],
            "key": [float value],
            "liveness": [float value],
            "loudness": [float value],
            "mode": [float value],
            "speechiness": [float value],
            "tempo": [float value],
            "time_signature": [float value],
            "valence": [float value],
            "popularity": [float value]
        },
        ...
    ],
    "mean_values": {
        "acousticness": {
            "mean": [mean acousticness float value for all tracks],
            "stddev": [mean acousticness float value for all tracks],
            "index": [column index integer value],
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    },
    "model": {
        "acousticness": [
            [coefficient index integer value],
            [coefficient float value]
        ],
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...,
        "intercept": [intercept float value]
    }
}
```

__Data Example:__

```
<page-number>: [page number to get]

{
    "songs": [
        {
            "track_id": "049RxG2laEl9U1PGYeIqLV",
            "acousticness": 8.11e-05,
            "danceability": 0.813,
            "duration_ms": 132742,
            "energy": 0.731,
            "instrumentalness": 0.91,
            "key": 11,
            "liveness": 0.0727,
            "loudness": -8.932,
            "mode": 1,
            "speechiness": 0.0697,
            "tempo": 124.031,
            "time_signature": 4,
            "valence": 0.944,
            "popularity": 7
        },
        ...
    ],
    "mean_values": {
        "acousticness": {
            "mean": 0.335554970038122,
            "stddev": 0.3430978160761376,
            "index": 0,
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    },
    "model": {
        "acousticness": [
            0,
            -1.12456456122314
        ],
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...,
        "intercept": 1.0730978160761376
    }
}
```

__Success Response:__

- __Code:__ 200 Ok
- __Content Example:__
    ```
    {
        "[track-id]": [distance from song as float value],
        ...
    }
    ```
- __Notes:__
  - Returns 100 tracks per page.

## Aggregate

__URL:__ `/api/v1.0/aggregate`

__Method:__ `POST`

__Auth Required:__ NO

__Data Contraints:__

```
{
    "songs": [
        {
            "acousticness": [float value],
            "danceability": [float value],
            "duration_ms": [float value],
            "energy": [float value],
            "instrumentalness": [float value],
            "key": [float value],
            "liveness": [float value],
            "loudness": [float value],
            "mode": [float value],
            "speechiness": [float value],
            "tempo": [float value],
            "time_signature": [float value],
            "valence": [float value],
            "popularity": [float value]
        },
        ...
    ]
}
```

__Data Example:__

```
{
    "songs": [
        {
            "acousticness": 8.11e-05,
            "danceability": 0.813,
            "duration_ms": 132742,
            "energy": 0.731,
            "instrumentalness": 0.91,
            "key": 11,
            "liveness": 0.0727,
            "loudness": -8.932,
            "mode": 1,
            "speechiness": 0.0697,
            "tempo": 124.031,
            "time_signature": 4,
            "valence": 0.944,
            "popularity": 7
        },
        ...
    ]
}
```

__Success Response:__

- __Code:__ 200 Ok
- __Content Example:__
    ```
    "mean_values": {
        "acousticness": {
            "mean": [float value],
            "stddev": [float value],
            "index": [integer value],
        },
        "danceability": ...,
        "duration_ms": ...,
        "energy": ...,
        "instrumentalness": ...,
        "key": ...,
        "liveness": ...,
        "loudness": ...,
        "mode": ...,
        "speechiness": ...,
        "tempo": ...,
        "time_signature": ...,
        "valence": ...,
        "popularity": ...
    }
    ```