import pytest
from fastapi.testclient import TestClient

from orderlab.api import create_app


@pytest.fixture
def client():
    with TestClient(create_app()) as test_client:
        yield test_client


def test_create_and_get_order(client):
    created = client.post("/orders", json={"price": 10_000, "quantity": 2})
    assert created.status_code == 201
    assert created.json() == {"id": 1, "subtotal": 20_000}

    found = client.get("/orders/1")
    assert found.status_code == 200
    assert found.json() == created.json()


@pytest.mark.parametrize(
    ("order", "field"),
    [
        ({"price": 100, "quantity": 0}, "quantity"),
        ({"price": -100, "quantity": 1}, "price"),
    ],
)
def test_invalid_order(client, order, field):
    response = client.post("/orders", json=order)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]


def test_missing_order(client):
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


def test_app_instances_keep_separate_orders(client):
    created = client.post("/orders", json={"price": 5_000, "quantity": 1})
    assert created.status_code == 201
    assert created.json() == {"id": 1, "subtotal": 5_000}

    with TestClient(create_app()) as other_client:
        assert other_client.get("/orders/1").status_code == 404
        other_order = other_client.post("/orders", json={"price": 3_000, "quantity": 2})
        assert other_order.status_code == 201
        assert other_order.json() == {"id": 1, "subtotal": 6_000}

    assert client.get("/orders/1").json() == created.json()
