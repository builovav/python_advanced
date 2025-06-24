import random

import factory

from flaskr.main.app import db
from flaskr.main.models import Clients, Parkings


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Clients
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyAttribute(lambda c: random.choice([True, False]))
    if credit_card:
        credit_card = factory.Faker("credit_card_number")  # type: ignore
    car_number = factory.Faker("bothify", text="###")


COUNT_PLACES = random.randrange(1, 999)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parkings
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.LazyAttribute(lambda o: random.choice([True, False]))
    count_places = COUNT_PLACES
    count_available_places = factory.lazy_attribute(
        lambda c: random.randrange(0, COUNT_PLACES)
    )
