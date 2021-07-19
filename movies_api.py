from flask import Flask, jsonify, request
from demographic_filtering import output
from storage import all_movies, liked_movies, non_liked_movies, non_match_movies
from content_filtering import get_recommendations
import csv


app = Flask(__name__)
# all_movies = []

@app.route('/get-movie')
def get_movie():
    global all_movies
    movie_data = {"title": all_movies[0][19],
                  "poster_link": all_movies[0][27],
                  "release_date": all_movies[0][13],
                  "duration": all_movies[0][15],
                  "rating": all_movies[0][20],
                  "overview": all_movies[0][9]}
    return jsonify({'data': movie_data, 'status':'Sucsess'}), 201


@app.route('/liked-movie', methods=["POST"])
def liked_movie():
    global all_movies
    movies = all_movies[0]
    liked_movies.append(movies)
    all_movies.pop(0)
    return jsonify({'status': 'Sucsess'}), 201


@app.route('/non-liked-movie', methods=["POST"])
def dis_liked_movie():
    global all_movies
    movies = all_movies[0]
    non_liked_movies.append(movies)
    all_movies.pop(0)
    return jsonify({'status': 'Sucsess'}), 201


@app.route('/did-not-match', methods=["POST"])
def non_match():
    global all_movies
    movies = all_movies[0]
    non_match_movies.append(movies)
    all_movies.pop(0)
    return jsonify({'status': 'Sucsess'}), 201


@app.route('/popular-movies')
def popular_movies():
    movie_data = []
    for movie in output:
        z = {"title": movie[0],
             "poster_link": movie[1],
             "release_date": movie[2],
             "duration": movie[3] or 'N/A',
             "rating": movie[4],
             "overview": movie[5]}
        movie_data.append(z)
    return jsonify({
        'data': movie_data,
        'status': "Sucsess"
    }), 200


@app.route('/recomendations')
def recomendations():
    all_recomended=[]
    for liked_movie in liked_movies:
        output= get_recommendations(liked_movie[19])
        for data in output:
            all_recomended.append(data)
    import itertools
    all_recomended.sort()
    all_recomended=list(all_recomended for all_recomended,_ in itertools.groupby(all_recomended))
    movie_data=[]
    for recomendation in all_recomended:
        d={
            "title":recomendation[0],
            "poster_link":recomendation[1],
            "release_date":recomendation[2],
            "duration":recomendation[3] or 'N/A', 
            "rating":recomendation[4], 
            "overview":recomendation[5]
            }
        movie_data.append(d)
    return jsonify({
        'data':movie_data,
        'status':'Sucsess'
    }),200

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
