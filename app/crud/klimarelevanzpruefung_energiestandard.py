from app.crud.base import CRUDBase
from app.models.klimarelevanzpruefung_energiestandard import (
    KlimarelevanzpruefungEnergiestandard as Model,
)
from app.schemas.klimarelevanzpruefung_energiestandard import (
    KlimarelevanzpruefungEnergiestandardCreate as CreateSchema,
    KlimarelevanzpruefungEnergiestandardUpdate as UpdateSchema,
)


class CRUDKlimarelevanzpruefungEnergiestandard(
    CRUDBase[Model, CreateSchema, UpdateSchema]
):
    def __init__(self):
        super().__init__(Model)


crud_klimarelevanzpruefung_energiestandard = CRUDKlimarelevanzpruefungEnergiestandard()
