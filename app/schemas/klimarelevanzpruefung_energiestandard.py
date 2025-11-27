from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungEnergiestandardBase(BaseModel):

    name: str = Field(..., description="The name of the Gemeinde.")


class KlimarelevanzpruefungEnergiestandardCreate(
    KlimarelevanzpruefungEnergiestandardBase
):
    pass


class KlimarelevanzpruefungEnergiestandardUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Aktualisierter Name des Items")


class KlimarelevanzpruefungEnergiestandardRead(
    KlimarelevanzpruefungEnergiestandardBase
):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item.")
