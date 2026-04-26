from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import requests

app = Flask(__name__)
CORS(app)

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

API_KEY = "YOUR_API_KEY"

def fetch_poster(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    data = requests.get(url).json()

    if data['results']:
        poster = data['results'][0].get('poster_path')
        if poster:
            return "https://image.tmdb.org/t/p/w500" + poster

    return "https://via.placeholder.com/300x450"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except:
        return []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    result = []
    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        result.append({
            "title": title,
            "poster": fetch_poster(title)
        })

    return result

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend_api():
    movie = request.json['movie']
    return jsonify({"recommendations": recommend(movie)})

if __name__ == "__main__":
    app.run(debug=True)
