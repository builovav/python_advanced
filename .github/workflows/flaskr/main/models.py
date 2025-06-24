from typing import Any, Dict

from sqlalchemy import UniqueConstraint

from flaskr.main.app import db


class Clients(db.Model):  # type: ignore
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=False)
    car_number = db.Column(db.String(10), nullable=False)
    client_id = db.relationship("Clientparking", back_populates="client")

    def __repr__(self):
        return f"Клиент {self.name, self.surname, self.car_number}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parkings(db.Model):  # type: ignore
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)
    parking_id = db.relationship("Clientparking", back_populates="parking")

    def __repr__(self):
        return f"Парковка: {
            self.address, self.opened,
            self.count_places, self.count_available_places
        }"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Clientparking(db.Model):  # type: ignore
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"), nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    client = db.relationship("Clients", back_populates="client_id")
    parking = db.relationship("Parkings", back_populates="parking_id")
    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    def __repr__(self):
        return f"Клиент {self.client.name, self.client.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {
            c.client.name: getattr(self, c.client.name) for c in self.__table__.columns
        }
