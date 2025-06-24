import datetime
from datetime import timedelta
import pytest
from sqlalchemy import UniqueConstraint

from flaskr.main.app import create_app, db as _db
from flaskr.main.models import Clients, Parkings, Clientparking


@pytest.fixture#(scope="session")
def app():
    _app = create_app()

    with _app.app_context():
        _db.create_all()
        client = Clients(
            id=5,
            name="name",
            surname="surname",
            credit_card="credit_card",
            car_number="car_number"
        )
        parking = Parkings(
            id=4,
            address="address",
            count_places=10,
            count_available_places=5,
            opened=0,
        )
        client_parking = Clientparking(
            id=4,
            client_id=4,
            parking_id=4,
            time_in=datetime.datetime.now() - timedelta(0, 3600),
            time_out=datetime.datetime.now(),
            __table_args__=(UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),)
            )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()

@pytest.fixture
def client(app):
    client = app.test_client()
    yield  client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db



