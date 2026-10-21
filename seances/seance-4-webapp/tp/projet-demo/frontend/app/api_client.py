import os
from typing import Any

import httpx


class ApiError(Exception):
    def __init__(self, status_code: int, detail: Any):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"API error {status_code}: {detail}")

    def messages(self) -> list[str]:
        if isinstance(self.detail, str):
            return [self.detail]
        if isinstance(self.detail, list):
            return [
                f"{error.get('loc', ['champ'])[-1]} : {error.get('msg', 'valeur invalide')}"
                for error in self.detail
                if isinstance(error, dict)
            ]
        return ["Une erreur est survenue."]


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = httpx.request(
                method, f"{self.base_url}{path}", timeout=5, **kwargs
            )
        except httpx.HTTPError as exc:
            raise ApiError(503, "Le backend est indisponible.") from exc
        if response.is_error:
            try:
                detail = response.json().get("detail", "Erreur du backend.")
            except ValueError:
                detail = "Erreur du backend."
            raise ApiError(response.status_code, detail)
        if response.status_code == 204:
            return None
        return response.json()

    def list_items(self) -> list[dict[str, Any]]:
        return self._request("GET", "/items")

    def get_item(self, item_id: int) -> dict[str, Any]:
        return self._request("GET", f"/items/{item_id}")

    def create_item(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/items", json=data)

    def list_reservations(self, item_id: int) -> list[dict[str, Any]]:
        return self._request("GET", "/reservations", params={"item_id": item_id})

    def create_reservation(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/reservations", json=data)

    def cancel_reservation(self, reservation_id: int) -> dict[str, Any]:
        return self._request(
            "PATCH",
            f"/reservations/{reservation_id}",
            json={"statut": "annulee"},
        )


api_client = ApiClient(os.environ["API_BASE_URL"])
