from flask import Flask, render_template, request, jsonify, make_response
from flasgger import Swagger
import json

app = Flask(__name__)
swagger = Swagger(app)

PORT = 3201
HOST = '0.0.0.0'

# charge le fichier JSON contenant les utilisateurs
with open('./databases/users.json', "r") as jsf:
    users = json.load(jsf)["users"]

# sauvegarde les utilisateurs dans le fichier
def write(users):
    with open('./databases/users.json', 'w') as f:
        json.dump({"users": users}, f)

# page d’accueil du service
@app.route("/", methods=['GET'])
def home():
    """
    Home endpoint
    ---
    responses:
      200:
        description: Welcome message
        content:
          text/html:
            schema:
              type: string
    """
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

# retourne tous les utilisateurs en JSON brut
@app.route("/users/json", methods=['GET'])
def get_json():
    """
    Get all users
    ---
    responses:
      200:
        description: List of users
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  last_active:
                    type: integer
    """
    return jsonify(users)

# retourne un utilisateur à partir de son ID
@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    """
    Get user by ID
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
        description: ID of the user
    responses:
      200:
        description: User found
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                last_active:
                  type: integer
      404:
        description: User not found
    """
    for user in users:
        if str(user["id"]) == str(userid):
            return jsonify(user), 200
    return jsonify({"error": "User ID not found"}), 404

# retourne un utilisateur à partir de son nom
@app.route("/users/userbyname", methods=['GET'])
def get_user_byname():
    """
    Get user by name
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: Name of the user
    responses:
      200:
        description: User found
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                last_active:
                  type: integer
      500:
        description: User name not found
    """
    json_res = ""
    if request.args:
        req = request.args
        for user in users:
            if str(user["name"]) == str(req["name"]):
                json_res = user

    if not json_res:
        res = make_response(jsonify({"error": "User name not found"}), 500)
    else:
        res = make_response(jsonify(json_res), 200)
    return res

# ajoute un utilisateur
@app.route("/users/<userid>", methods=['POST'])
def add_user(userid):
    """
    Add a new user
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
        description: ID of the new user
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              last_active:
                type: integer
    responses:
      200:
        description: User added successfully
      500:
        description: User ID already exists
    """
    req = request.get_json()

    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User ID already exists"}), 500)

    users.append(req)
    write(users)
    return make_response(jsonify({"message": "User added"}), 200)

# modifie le nom de l'utilisateur à partir de son ID
@app.route("/users/<userid>/<name>", methods=['PUT'])
def update_user_name(userid, name):
    """
    Update a user's name
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
        description: ID of the user
      - name: name
        in: path
        type: string
        required: true
        description: New name for the user
    responses:
      200:
        description: User updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                last_active:
                  type: integer
      500:
        description: User ID not found
    """
    for user in users:
        if str(user["id"]) == str(userid):
            user["name"] = name
            write(users)
            return make_response(jsonify(user), 200)

    return make_response(jsonify({"error": "user ID not found"}), 500)

# supprime un utilisateur
@app.route("/users/<userid>", methods=['DELETE'])
def del_user(userid):
    """
    Delete a user by ID
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
        description: ID of the user to delete
    responses:
      200:
        description: User deleted successfully
      500:
        description: User ID not found
    """
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            write(users)
            return make_response(jsonify(user), 200)

    return make_response(jsonify({"error": "user ID not found"}), 500)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
