import random

import factory

from app.models import Client, Parking, db


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyAttribute(
        lambda x: "1234-5678" if random.random() > 0.5 else None
    )
    car_number = factory.Faker("bothify", text="?###??")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = True
    count_places = 10
    count_available_places = factory.LazyAttribute(lambda o: o.count_places)
