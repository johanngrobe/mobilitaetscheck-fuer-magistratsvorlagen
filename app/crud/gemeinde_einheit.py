from app.crud.base import CRUDBase
from app.models.gemeinde_einheit import GemeindeEinheit as Model
from app.schemas.gemeinde_einheit import (
    GemeindeEinheitCreate as CreateSchema,
    GemeindeEinheitUpdate as UpdateSchema,
)


class CRUDGemeindeEinheit(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_gemeinde_einheit = CRUDGemeindeEinheit()
