from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

# charge le fichier JSON contenant le planning
with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]

# sauvegarde le planning dans le fichier
def write(times):
    with open('{}/databases/times.json'.format("."), 'w') as f:
        full = {}
        full['schedule']=times
        json.dump(full, f)

# page d’accueil du service
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

# retourne tout le planning en JSON brut
@app.route("/schedule/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(schedule), 200)
    return res

# récupère les films programmés pour une date précise
@app.route("/schedule/<date>", methods=['GET'])
def get_movies_by_date(date):
    for movies_date in schedule:
        if str(movies_date["date"]) == str(date):
            res = make_response(jsonify(movies_date["movies"]),200) # renvoi tous les movies direct suivant la date
            return res
    return make_response(jsonify({"error":"No movies found with this date"}),500)

# récupère toutes les dates où un film est projeté (via son ID en query param)
@app.route("/schedule", methods=['GET'])
def get_schedule_by_movie_id():
    movie_id = request.args.get("id") # récupère ?id=xxxx
    
    if not movie_id:
        return make_response(jsonify({"error": "missing 'id' parameter"}), 400)

    # récupère toutes les dates où ce film apparaît
    dates = [movies_date["date"] for movies_date in schedule if movie_id in movies_date["movies"]]

    if not dates:
        return make_response(jsonify({"error": "no schedule found for this movie id"}), 404)

    return make_response(jsonify({
        "movie_id": movie_id,
        "dates": dates
    }), 200)

# ajoute une nouvelle date (échoue si la date existe déjà)
@app.route("/schedule/<date_id>", methods=['POST'])
def add_date_schedule(date_id):
    req = request.get_json()

    # vérifie si la date existe déjà
    for movies_date in schedule:
        if str(movies_date["date"]) == str(date_id):
            return make_response(jsonify({"error": "schedule date already exists"}), 500)

    # ajoute la nouvelle entrée (soit avec données du body, soit vide avec seulement l'ID)
    new_entry = {
        "date": date_id,
        "movies": req.get("movies", []) # si pas fourni, on met []
    }
    schedule.append(new_entry)
    write(schedule)

    return make_response(jsonify({"message": "schedule date added"}), 200)

# ajoute un film à une date (crée la date si elle n’existe pas)
@app.route("/schedule/<date>/movies", methods=['POST'])
def add_movie_to_date(date):
    req = request.get_json()
    movie_id = req.get("movie_id")

    if not movie_id:
        return make_response(jsonify({"error": "missing 'movie_id' in body"}), 400)

    # cherche si la date existe déjà
    for movies_date in schedule:
        if str(movies_date["date"]) == str(date):
            # si le film existe déjà dans la liste
            if movie_id in movies_date["movies"]:
                return make_response(jsonify({"error": "movie already scheduled for this date"}), 500)
            
            # sinon on ajoute
            movies_date["movies"].append(movie_id)
            write(schedule)
            return make_response(jsonify({"message": "movie added to existing date"}), 200)

    # si la date n'existe pas : on la crée
    new_entry = {
        "date": date,
        "movies": [movie_id]
    }
    schedule.append(new_entry)
    write(schedule)

    return make_response(jsonify({"message": "new date created and movie added"}), 200)

# supprime une date complète (tous les films inclus)
@app.route("/schedule/<date_id>", methods=['DELETE'])
def delete_date(date_id):
    global schedule
    new_schedule = [s for s in schedule if str(s["date"]) != str(date_id)]

    if len(new_schedule) == len(schedule):
        return make_response(jsonify({"error": "date not found"}), 404)

    schedule = new_schedule
    write(schedule)
    return make_response(jsonify({"message": f"date {date_id} deleted"}), 200)

# supprime un film d’une date précise
@app.route("/schedule/<date_id>/movies/<movie_id>", methods=['DELETE'])
def delete_movie_from_date(date_id, movie_id):
    for s in schedule:
        if str(s["date"]) == str(date_id):
            if movie_id in s["movies"]:
                s["movies"].remove(movie_id)
                write(schedule)
                return make_response(jsonify({"message": f"movie {movie_id} removed from date {date_id}"}), 200)
            return make_response(jsonify({"error": "movie not found in this date"}), 404)
    
    return make_response(jsonify({"error": "date not found"}), 404)


# supprime un film de toutes les dates
@app.route("/schedule/movies/<movie_id>", methods=['DELETE'])
def delete_movie_from_all_dates(movie_id):
    found = False
    for s in schedule:
        if movie_id in s["movies"]:
            s["movies"].remove(movie_id)
            found = True

    if not found:
        return make_response(jsonify({"error": "movie not found in any date"}), 404)

    write(schedule)
    return make_response(jsonify({"message": f"movie {movie_id} removed from all dates"}), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
