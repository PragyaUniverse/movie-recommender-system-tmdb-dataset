import pickle
import json

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    for i in movies_list:
        recommended.append(movies.iloc[i[0]].title)

    return recommended

def handler(request):
    movie = request.args.get("movie")

    if not movie:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Enter a movie"})
        }

    try:
        recs = recommend(movie)
        return {
            "statusCode": 200,
            "body": json.dumps({"recommendations": recs})
        }
    except:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Movie not found"})
        }
