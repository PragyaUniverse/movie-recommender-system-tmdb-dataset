from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import requests

app = Flask(__name__)
CORS(app)

# Load your saved files
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# 🔑 TMDB API KEY (get from https://www.themoviedb.org/)
API_KEY = "YOUR_API_KEY_HERE"

def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    data = requests.get(url).json()

    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    
    return "https://via.placeholder.com/300x450?text=No+Image"


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except:
        return []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommendations = []
    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommendations.append({
            "title": title,
            "poster": fetch_poster(title)
        })

    return recommendations


@app.route('/recommend', methods=['POST'])
def recommend_api():
    data = request.get_json()
    movie = data['movie']

    results = recommend(movie)

    return jsonify({
        "recommendations": results
    })


if __name__ == '__main__':
    app.run(debug=True)
