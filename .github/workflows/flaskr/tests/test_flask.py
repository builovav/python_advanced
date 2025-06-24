import datetime
import json

import pytest


def test_first(client) -> None:
    resp = client.get("/")
    data = resp.data.decode()
    assert resp.status_code == 200
    assert data == "Hello, World!"


def test_math_route(client) -> None:
    resp = client.get("/test_route?number=8")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert data == 64


def test_user(client) -> None:

    resp = client.get("/clients/5")
    assert resp.status_code == 200
    assert resp.json == {
        "id": 5,
        "name": "name",
        "surname": "surname",
        "credit_card": "credit_card",
        "car_number": "car_number",
    }


def test_users(client) -> None:
    resp = client.get("/clients")
    assert resp.status_code == 200
    assert resp.json == [
        {
            "id": 5,
            "name": "name",
            "surname": "surname",
            "credit_card": "credit_card",
            "car_number": "car_number",
        }
    ]


def test_parkings(client) -> None:
    resp = client.get("/parkings")
    assert resp.status_code == 200
    assert resp.json == [
        {
            "id": 4,
            "address": "address",
            "count_places": 10,
            "count_available_places": 5,
            "opened": 0,
        }
    ]


def test_create_client(client) -> None:
    client_data = {
        "name": "Alex",
        "surname": "Buylov",
        "credit_card": "123 456 789",
        "car_number": "777",
    }
    resp = client.post("/clients", data=client_data)
    assert resp.status_code == 201


def test_create_parking(client) -> None:
    parking_data = {
        "address": "Kanzas",
        "count_places": 10,
        "count_available_place": 5,
        "opened": True,
    }
    resp = client.post("/parkings", data=parking_data)
    assert resp.status_code == 201


@pytest.mark.parking
def test_client_parking(client) -> None:
    client_parking_data = {
        "client_id": "1",
        "parking_id": "2",
        "time_in": datetime.datetime.now(),
    }
    resp = client.post("/client_parkings", data=client_parking_data)
    assert resp.status_code == 201


def test_client_parking_delete(client) -> None:
    client_parking_data = {
        "client_id": "1",
        "parking_id": "2",
        "time_out": datetime.datetime.now(),
    }
    resp = client.post("/client_parkings", data=client_parking_data)
    assert resp.status_code == 201


@pytest.mark.parametrize(
    "route", ["/test_route?number=8", "/clients/5", "/clients", "/"]
)
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200
