from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'
SCHEDULE_URL = "http://localhost:3202" # service Schedule
MOVIE_URL   = "http://localhost:3200" # service Movie

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]

def write(bookings_data):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        full = {}
        full['bookings'] = bookings_data
        json.dump(full, f)

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

# récupère toutes les réservations
@app.route("/bookings", methods=['GET'])
def get_all_bookings():
    return make_response(jsonify(bookings), 200)

# récupère les réservations d’un utilisateur
@app.route("/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    for b in bookings:
        if b["userid"] == userid:
            return make_response(jsonify(b), 200)
    return make_response(jsonify({"error": "user not found"}), 404)

# ajoute une réservation pour un utilisateur
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking(userid):
    req = request.get_json()
    date = req.get("date")
    movie_id = req.get("movie_id")

    if not date or not movie_id:
        return make_response(jsonify({"error": "missing 'date' or 'movie_id'"}), 400)

    # vérifie auprès de Schedule que le film est dispo à cette date
    r = requests.get(f"{SCHEDULE_URL}/schedule/{date}") # appele microservice de Schedule
    if r.status_code != 200:
        return make_response(jsonify({"error": "date not found in schedule"}), 404)

    movies_for_date = r.json()
    if movie_id not in movies_for_date:
        return make_response(jsonify({"error": "movie not available at this date"}), 400)

    # si l’utilisateur existe déjà
    for b in bookings:
        if b["userid"] == userid:
            for d in b["dates"]:
                if d["date"] == date:
                    if movie_id in d["movies"]:
                        return make_response(jsonify({"error": "booking already exists"}), 400)
                    d["movies"].append(movie_id)
                    write(bookings)
                    return make_response(jsonify({"message": "movie booked"}), 200)
            # sinon nouvelle date pour l’utilisateur
            b["dates"].append({"date": date, "movies": [movie_id]})
            write(bookings)
            return make_response(jsonify({"message": "movie booked with new date"}), 200)

    # si l’utilisateur n’existe pas encore -> on le crée
    new_booking = {
        "userid": userid,
        "dates": [
            {"date": date, "movies": [movie_id]}
        ]
    }
    bookings.append(new_booking)
    write(bookings)
    return make_response(jsonify({"message": "new user created and booking added"}), 200)

# supprime une réservation (film spécifique pour une date d’un user)
@app.route("/bookings/<userid>/<date>/<movie_id>", methods=['DELETE'])
def delete_booking(userid, date, movie_id):
    for b in bookings:
        if b["userid"] == userid:
            for d in b["dates"]:
                if d["date"] == date:
                    if movie_id in d["movies"]:
                        d["movies"].remove(movie_id)
                        write(bookings)
                        return make_response(jsonify({"message": "booking deleted"}), 200)
                    return make_response(jsonify({"error": "movie not found in this booking"}), 404)
    return make_response(jsonify({"error": "booking not found"}), 404)

# supprime toutes les réservations d’un utilisateur
@app.route("/bookings/<userid>", methods=['DELETE'])
def delete_user_bookings(userid):
    global bookings
    new_bookings = [b for b in bookings if b["userid"] != userid]
    if len(new_bookings) == len(bookings):
        return make_response(jsonify({"error": "user not found"}), 404)

    bookings = new_bookings
    write(bookings)
    return make_response(jsonify({"message": f"all bookings deleted for {userid}"}), 200)

# récupère les réservations d’un utilisateur avec détail des films
@app.route("/bookings/<userid>/details", methods=['GET'])
def get_user_booking_details(userid):
    for b in bookings:
        if b["userid"] == userid:
            detailed = {"userid": userid, "dates": []}
            for d in b["dates"]:
                movies_detail = []
                for m in d["movies"]:
                    r = requests.get(f"{MOVIE_URL}/movies/{m}") # appele microservice de Movie
                    if r.status_code == 200:
                        movies_detail.append(r.json())
                    else:
                        movies_detail.append({"id": m, "error": "movie not found"})
                detailed["dates"].append({
                    "date": d["date"],
                    "movies": movies_detail
                })
            return make_response(jsonify(detailed), 200)
    return make_response(jsonify({"error": "user not found"}), 404)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
