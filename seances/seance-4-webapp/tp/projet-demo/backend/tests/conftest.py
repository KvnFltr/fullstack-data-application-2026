from collections.abc import Iterator
from dataclasses import dataclass, fields
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items, reservations


@dataclass
class Storage:
    items: dict[int, dict[str, Any]]
    reservations: dict[int, dict[str, Any]]

    def reset_all(self) -> None:
        for field in fields(self):
            getattr(self, field.name).clear()


@pytest.fixture
def storage() -> Iterator[Storage]:
    current = Storage(items=items.FAKE_DB, reservations=reservations.FAKE_DB)
    current.reset_all()
    yield current
    current.reset_all()


@pytest.fixture
def client(storage: Storage) -> TestClient:
    return TestClient(app)


@pytest.fixture
def item_velo(client: TestClient) -> dict[str, Any]:
    response = client.post(
        "/items",
        json={
            "titre": "Vélo de ville",
            "description": "Trois vitesses",
            "tarif_jour": 8.5,
        },
    )
    assert response.status_code == 201
    return response.json()
