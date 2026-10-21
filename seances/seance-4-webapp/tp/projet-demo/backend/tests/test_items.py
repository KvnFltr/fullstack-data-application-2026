from typing import Any

import pytest
from fastapi.testclient import TestClient


def test_lister_items_filtre_et_limite(
    client: TestClient, storage: Any
) -> None:
    storage.items.update(
        {
            1: {"id": 1, "titre": "Vélo rouge", "description": None, "tarif_jour": 8.0, "disponible": True},
            2: {"id": 2, "titre": "Tente", "description": None, "tarif_jour": 12.0, "disponible": False},
            3: {"id": 3, "titre": "Vélo bleu", "description": None, "tarif_jour": 9.0, "disponible": True},
        }
    )

    response = client.get("/items", params={"q": "vélo", "disponible": True, "limit": 1})

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [1]


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"titre": "ab", "tarif_jour": 8.5}, "titre"),
        ({"titre": "Vélo", "tarif_jour": 0}, "tarif_jour"),
        ({"titre": "Vélo", "tarif_jour": 8.5, "couleur": "rouge"}, "couleur"),
    ],
)
def test_creation_item_invalide_renvoie_422(
    client: TestClient, payload: dict[str, Any], field: str
) -> None:
    response = client.post("/items", json=payload)

    assert response.status_code == 422
    assert field in [error["loc"][-1] for error in response.json()["detail"]]


def test_patch_item_ne_remplace_que_les_champs_fournis(
    client: TestClient, item_velo: dict[str, Any]
) -> None:
    response = client.patch(
        f"/items/{item_velo['id']}", json={"titre": "Vélo pliant"}
    )

    assert response.status_code == 200
    assert response.json()["titre"] == "Vélo pliant"
    assert response.json()["description"] == "Trois vitesses"
    assert response.json()["tarif_jour"] == 8.5


def test_remplacement_item_inexistant_renvoie_404(client: TestClient) -> None:
    response = client.put(
        "/items/999",
        json={"titre": "Vélo", "tarif_jour": 8.5},
    )

    assert response.status_code == 404


def test_suppression_item_est_visible_a_la_lecture(
    client: TestClient, item_velo: dict[str, Any]
) -> None:
    item_id = item_velo["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 204
    assert client.get(f"/items/{item_id}").status_code == 404


@pytest.mark.parametrize(
    "path",
    ["/items/0", "/items/-1", "/items/abc"],
)
def test_identifiant_item_invalide_renvoie_422(
    client: TestClient, path: str
) -> None:
    response = client.get(path)

    assert response.status_code == 422
