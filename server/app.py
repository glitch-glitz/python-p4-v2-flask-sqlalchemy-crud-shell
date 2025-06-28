from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from models import db, Pet

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


# Route to get all pets
@app.route("/pets", methods=["GET"])
def get_pets():
    pets = Pet.query.all()
    pets_list = [
        {"id": pet.id, "name": pet.name, "species": pet.species} for pet in pets
    ]
    return jsonify(pets_list), 200


# Route to create a new pet
@app.route("/pets", methods=["POST"])
def create_pet():
    data = request.get_json()
    if not data or not "name" in data or not "species" in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_pet = Pet(name=data["name"], species=data["species"])
    db.session.add(new_pet)
    db.session.commit()
    return jsonify(
        {"id": new_pet.id, "name": new_pet.name, "species": new_pet.species}
    ), 201


# Route to get a single pet by ID
@app.route("/pets/<int:id>", methods=["GET"])
def get_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        abort(404, description="Pet not found")
    return jsonify({"id": pet.id, "name": pet.name, "species": pet.species}), 200


# Route to update a pet by ID
@app.route("/pets/<int:id>", methods=["PATCH"])
def update_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        abort(404, description="Pet not found")

    data = request.get_json()
    if "name" in data:
        pet.name = data["name"]
    if "species" in data:
        pet.species = data["species"]

    db.session.commit()
    return jsonify({"id": pet.id, "name": pet.name, "species": pet.species}), 200


# Route to delete a pet by ID
@app.route("/pets/<int:id>", methods=["DELETE"])
def delete_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        abort(404, description="Pet not found")

    db.session.delete(pet)
    db.session.commit()
    return jsonify({"message": f"Pet {id} deleted"}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
