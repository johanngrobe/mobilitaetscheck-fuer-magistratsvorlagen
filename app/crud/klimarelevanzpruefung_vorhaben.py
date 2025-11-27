from app.crud.base import CRUDBase
from app.models.klimarelevanzpruefung_vorhaben import (
    KlimarelevanzpruefungVorhaben as Model,
)
from app.schemas.klimarelevanzpruefung_vorhaben import (
    KlimarelevanzpruefungVorhabenCreate as CreateSchema,
    KlimarelevanzpruefungVorhabenUpdate as UpdateSchema,
)


class CRUDKlimarelevanzpruefungVorhaben(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimarelevanzpruefung_vorhaben = CRUDKlimarelevanzpruefungVorhaben()
