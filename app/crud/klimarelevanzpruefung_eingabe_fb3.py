from app.crud.base import CRUDBase
from app.models.klimarelevanzpruefung_eingabe_fb3 import (
    KlimarelevanzpruefungEingabeFb3 as Model,
)
from app.schemas.klimarelevanzpruefung_eingabe_fb3 import (
    KlimarelevanzpruefungEingabeFb3Create as CreateSchema,
    KlimarelevanzpruefungEingabeFb3Update as UpdateSchema,
)


class CRUDKlimarelevanzpruefungEingabeFb3(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimarelevanzpruefung_eingabe_fb3 = CRUDKlimarelevanzpruefungEingabeFb3()
