from app.crud.base import CRUDBase
from app.models.bool_erweitert import BoolErweitert as Model
from app.schemas.bool_erweitert import (
    BoolErweitertCreate as CreateSchema,
    BoolErweitertUpdate as UpdateSchema,
)


class CRUDBoolErweitert(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_bool_erweitert = CRUDBoolErweitert()
