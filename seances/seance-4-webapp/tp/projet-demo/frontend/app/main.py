from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api_client import ApiError
from app.routers import items, reservations
from app.templating import templates

app = FastAPI(title="GearShare Frontend")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(items.router)
app.include_router(reservations.router)


@app.get("/")
def home() -> RedirectResponse:
    return RedirectResponse(url="/items", status_code=303)


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    message = "Service indisponible." if exc.status_code == 503 else exc.messages()[0]
    return templates.TemplateResponse(
        request=request,
        name="erreur.html",
        context={"message": message},
        status_code=exc.status_code,
    )
