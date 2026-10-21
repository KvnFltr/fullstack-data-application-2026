from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.reservation import ReservationCreate


def test_reservation_valide_est_acceptee() -> None:
    reservation = ReservationCreate(
        item_id=1,
        date_debut=date(2026, 9, 1),
        date_fin=date(2026, 9, 5),
    )

    assert reservation.date_fin > reservation.date_debut


def test_reservation_aux_dates_incoherentes_est_refusee() -> None:
    with pytest.raises(ValidationError):
        ReservationCreate(
            item_id=1,
            date_debut=date(2026, 9, 5),
            date_fin=date(2026, 9, 1),
        )


def test_item_update_sans_champ_est_vide() -> None:
    assert ItemUpdate().model_dump(exclude_unset=True) == {}


def test_item_create_refuse_les_champs_inconnus() -> None:
    with pytest.raises(ValidationError):
        ItemCreate(titre="Vélo", tarif_jour=8.5, couleur="rouge")
