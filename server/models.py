from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": self.price,
            "is_in_stock": self.is_in_stock,
        }