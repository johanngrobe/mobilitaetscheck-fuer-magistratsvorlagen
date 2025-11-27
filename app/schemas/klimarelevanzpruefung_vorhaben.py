from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungVorhabenBase(BaseModel):

    name: str = Field(..., description="The name of the Gemeinde.")


class KlimarelevanzpruefungVorhabenCreate(KlimarelevanzpruefungVorhabenBase):
    pass


class KlimarelevanzpruefungVorhabenUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Aktualisierter Name des Items")


class KlimarelevanzpruefungVorhabenRead(KlimarelevanzpruefungVorhabenBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item.")
    energiestandards: Optional[list["KlimarelevanzpruefungEnergiestandardRead"]] = (
        Field(None, description="List of associated Energiestandard objects.")
    )


from app.schemas.klimarelevanzpruefung_energiestandard import (
    KlimarelevanzpruefungEnergiestandardRead,
)
