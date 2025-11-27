from app.crud.base import CRUDBase
from app.models.klimarelevanzpruefung_eingabe_fb2 import (
    KlimarelevanzpruefungEingabeFb2 as Model,
)
from app.schemas.klimarelevanzpruefung_eingabe_fb2 import (
    KlimarelevanzpruefungEingabeFb2Create as CreateSchema,
    KlimarelevanzpruefungEingabeFb2Update as UpdateSchema,
)


class CRUDKlimarelevanzpruefungEingabeFb2(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimarelevanzpruefung_eingabe_fb2 = CRUDKlimarelevanzpruefungEingabeFb2()
