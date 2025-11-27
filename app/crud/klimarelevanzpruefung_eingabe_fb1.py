from app.crud.base import CRUDBase
from app.models.klimarelevanzpruefung_eingabe_fb1 import (
    KlimarelevanzpruefungEingabeFb1 as Model,
)
from app.schemas.klimarelevanzpruefung_eingabe_fb1 import (
    KlimarelevanzpruefungEingabeFb1Create as CreateSchema,
    KlimarelevanzpruefungEingabeFb1Update as UpdateSchema,
)


class CRUDKlimarelevanzpruefungEingabeFb1(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimarelevanzpruefung_eingabe_fb1 = CRUDKlimarelevanzpruefungEingabeFb1()
