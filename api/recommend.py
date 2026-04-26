import os
import pickle
import json

BASE_DIR = os.path.dirname(__file__)

movies = pickle.load(open(os.path.join(BASE_DIR, '../movie_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, '../similarity.pkl'), 'rb'))

def recommend(movie):
    # make search case-insensitive
    movie = movie.lower()

    matches = movies[movies['title'].str.lower() == movie]

    if matches.empty:
        return None

    movie_index = matches.index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended = [movies.iloc[i[0]].title for i in movies_list]

    return recommended


def handler(request):
    movie = request.args.get("movie")

    if not movie:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Enter a movie"})
        }

    recs = recommend(movie)

    if recs is None:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Movie not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"recommendations": recs})
    }
