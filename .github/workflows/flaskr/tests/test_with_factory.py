from flaskr.main.models import Clients, Parkings
from flaskr.tests.factories import ClientFactory, ParkingFactory


def test_create_client(app, db):
    client = ClientFactory()
    db.session.commit()
    assert client.id is not None
    assert len(db.session.query(Clients).all()) == 2


def test_create_parking(client, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert len(db.session.query(Parkings).all()) == 2
