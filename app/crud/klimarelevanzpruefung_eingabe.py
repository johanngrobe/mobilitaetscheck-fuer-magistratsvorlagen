from app.crud.base import CRUDBase
from app.models.klimarelevanzpruefung_eingabe import (
    KlimarelevanzpruefungEingabe as Model,
)
from app.schemas.klimarelevanzpruefung_eingabe import (
    KlimarelevanzpruefungEingabeCreate as CreateSchema,
    KlimarelevanzpruefungEingabeUpdate as UpdateSchema,
)


class CRUDKlimarelevanzpruefungEingabe(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimarelevanzpruefung_eingabe = CRUDKlimarelevanzpruefungEingabe()
