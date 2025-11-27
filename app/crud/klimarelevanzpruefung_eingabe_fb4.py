from app.crud.base import CRUDBase
from app.models.klimarelevanzpruefung_eingabe_fb4 import (
    KlimarelevanzpruefungEingabeFb4 as Model,
)
from app.schemas.klimarelevanzpruefung_eingabe_fb4 import (
    KlimarelevanzpruefungEingabeFb4Create as CreateSchema,
    KlimarelevanzpruefungEingabeFb4Update as UpdateSchema,
)


class CRUDKlimarelevanzpruefungEingabeFb4(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimarelevanzpruefung_eingabe_fb4 = CRUDKlimarelevanzpruefungEingabeFb4()
