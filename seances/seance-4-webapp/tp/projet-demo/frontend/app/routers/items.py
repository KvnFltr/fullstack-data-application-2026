from datetime import date

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api_client import ApiError, api_client
from app.templating import templates

router = APIRouter()


@router.get("/items", response_class=HTMLResponse)
def list_items(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="items/list.html",
        context={"items": api_client.list_items()},
    )


@router.get("/items/new", response_class=HTMLResponse)
def new_item_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="items/form.html",
        context={"errors": [], "values": {}},
    )


@router.post("/items", response_class=HTMLResponse)
def create_item(
    request: Request,
    titre: str = Form(...),
    description: str = Form(""),
    tarif_jour: float = Form(...),
    disponible: bool = Form(False),
):
    values = {
        "titre": titre,
        "description": description,
        "tarif_jour": tarif_jour,
        "disponible": disponible,
    }
    try:
        item = api_client.create_item(
            {**values, "description": description or None}
        )
    except ApiError as exc:
        if exc.status_code != 422:
            raise
        return templates.TemplateResponse(
            request=request,
            name="items/form.html",
            context={"errors": exc.messages(), "values": values},
            status_code=422,
        )
    return RedirectResponse(f"/items/{item['id']}", status_code=303)


@router.get("/items/{item_id}", response_class=HTMLResponse)
def item_detail(
    request: Request,
    item_id: int,
    errors: list[str] | None = None,
    reservation_values: dict[str, str] | None = None,
    confirmation: str | None = None,
    status_code: int = 200,
):
    item = api_client.get_item(item_id)
    return templates.TemplateResponse(
        request=request,
        name="items/detail.html",
        context={
            "item": item,
            "reservations": api_client.list_reservations(item_id),
            "errors": errors or [],
            "reservation_values": reservation_values or {},
            "confirmation": confirmation,
        },
        status_code=status_code,
    )
