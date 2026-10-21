from typing import Any

from fastapi.testclient import TestClient


def test_creer_reservation_puis_la_relire(
    client: TestClient, item_velo: dict[str, Any]
) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item_velo["id"],
            "date_debut": "2026-09-01",
            "date_fin": "2026-09-05",
        },
    )

    assert response.status_code == 201
    reservation = response.json()
    assert reservation["statut"] == "active"
    assert client.get(f"/reservations/{reservation['id']}").json() == reservation


def test_annuler_deux_fois_renvoie_409(
    client: TestClient, item_velo: dict[str, Any]
) -> None:
    creation = client.post(
        "/reservations",
        json={
            "item_id": item_velo["id"],
            "date_debut": "2026-09-01",
            "date_fin": "2026-09-05",
        },
    )
    reservation_id = creation.json()["id"]
    client.post(f"/reservations/{reservation_id}/annuler")

    response = client.post(f"/reservations/{reservation_id}/annuler")

    assert response.status_code == 409
    assert client.get(f"/reservations/{reservation_id}").json()["statut"] == "annulee"


def test_annulation_reservation_absente_renvoie_404(client: TestClient) -> None:
    response = client.post("/reservations/999/annuler")

    assert response.status_code == 404


def test_dates_incoherentes_renvoient_422(
    client: TestClient, item_velo: dict[str, Any]
) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item_velo["id"],
            "date_debut": "2026-09-05",
            "date_fin": "2026-09-01",
        },
    )

    assert response.status_code == 422


def test_lister_reservations_filtre_par_item(
    client: TestClient, item_velo: dict[str, Any]
) -> None:
    client.post(
        "/reservations",
        json={
            "item_id": item_velo["id"],
            "date_debut": "2026-09-01",
            "date_fin": "2026-09-05",
        },
    )

    response = client.get(
        "/reservations", params={"item_id": item_velo["id"], "limit": 1}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
