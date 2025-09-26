from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Ensure the table exists + seed one plant if missing
with app.app_context():
    db.create_all()
    if not Plant.query.first():
        sample = Plant(
            name="Live Oak",
            image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
            price=250.00,
            is_in_stock=True,
        )
        db.session.add(sample)
        db.session.commit()


@app.route("/")
def index():
    return "Welcome to the Plants API"


@app.route("/plants", methods=["GET", "POST"])
def plants():
    if request.method == "GET":
        all_plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in all_plants]), 200

    elif request.method == "POST":
        data = request.get_json()
        new_plant = Plant(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price"),
            is_in_stock=data.get("is_in_stock", True),
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201


@app.route("/plants/<int:id>", methods=["GET", "PATCH", "DELETE"])
def plant_by_id(id):
    plant = Plant.query.get(id)
    if not plant:
        return {"error": "Plant not found"}, 404

    if request.method == "GET":
        return jsonify(plant.to_dict()), 200

    elif request.method == "PATCH":
        data = request.get_json()
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]
        if "name" in data:
            plant.name = data["name"]
        if "price" in data:
            plant.price = data["price"]
        if "image" in data:
            plant.image = data["image"]
        db.session.commit()
        return jsonify(plant.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(plant)
        db.session.commit()
        return {}, 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)