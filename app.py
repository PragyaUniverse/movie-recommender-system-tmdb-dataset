from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

new = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/recommend')
def recommend():
    movie = request.args.get('movie')
    try:
        index = new[new['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        return jsonify([{"t": new.iloc[i[0]].title, "s": round(float(v)*100)} for i,v in [(d, d[1]) for d in distances[1:6]]])
    except:
        return jsonify([]), 404

@app.route('/movies')
def movies():
    return jsonify(new['title'].tolist())

if __name__ == '__main__':
    app.run(port=5000)
