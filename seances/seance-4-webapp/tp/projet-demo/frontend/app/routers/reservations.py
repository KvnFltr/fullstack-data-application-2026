from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app.api_client import ApiError, api_client
from app.routers.items import item_detail

router = APIRouter()


@router.post("/items/{item_id}/reservations")
def create_reservation(
    request: Request,
    item_id: int,
    date_debut: str = Form(...),
    date_fin: str = Form(...),
):
    values = {"date_debut": date_debut, "date_fin": date_fin}
    try:
        api_client.create_reservation(
            {"item_id": item_id, "date_debut": date_debut, "date_fin": date_fin}
        )
    except ApiError as exc:
        if exc.status_code != 422:
            raise
        return item_detail(
            request,
            item_id,
            errors=exc.messages(),
            reservation_values=values,
            status_code=422,
        )
    return RedirectResponse(
        f"/items/{item_id}?confirmation=Réservation créée.",
        status_code=303,
    )


@router.post("/reservations/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    item_id: int = Form(...),
    statut: str = Form(...),
):
    try:
        api_client.cancel_reservation(reservation_id)
    except ApiError as exc:
        if exc.status_code != 409:
            raise
        return RedirectResponse(
            f"/items/{item_id}?confirmation=Cette réservation est déjà annulée.",
            status_code=303,
        )
    return RedirectResponse(f"/items/{item_id}", status_code=303)
