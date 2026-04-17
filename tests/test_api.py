import pytest
from typing import Any

from .factories import ClientFactory, ParkingFactory


@pytest.mark.parametrize("url", ["/clients"])
def test_get_methods_status(client: Any, url: str) -> None:  # Добавили аннотации
    response = client.get(url)
    assert response.status_code == 200


def test_create_client_factory(client: Any, db: Any) -> None:
    client_data = {"name": "Ivan", "surname": "Ivanov"}
    response = client.post("/clients", json=client_data)
    assert response.status_code == 201
    assert "id" in response.json


@pytest.mark.parking
def test_parking_entry(client: Any, db: Any) -> None:
    p = ParkingFactory(opened=True, count_places=5)
    c = ClientFactory()
    db.session.commit()

    response = client.post(
        "/client_parkings", json={"client_id": c.id, "parking_id": p.id}
    )
    assert response.status_code == 201
    assert p.count_available_places == 4


@pytest.mark.parking
def test_parking_exit(client: Any, db: Any) -> None:
    p = ParkingFactory(count_places=5)
    c = ClientFactory(credit_card="4444")
    db.session.commit()

    client.post("/client_parkings", json={"client_id": c.id, "parking_id": p.id})
    response = client.delete(
        "/client_parkings", json={"client_id": c.id, "parking_id": p.id}
    )
    assert response.status_code == 200
    assert p.count_available_places == 5