from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungEingabeFb4Base(BaseModel):

    d1q1: str
    d2q1: str


class KlimarelevanzpruefungEingabeFb4Create(KlimarelevanzpruefungEingabeFb4Base):
    pass


class KlimarelevanzpruefungEingabeFb4Update(BaseModel):
    d1q1: Optional[str] = None
    d2q1: Optional[str] = None


class KlimarelevanzpruefungEingabeFb4Read(KlimarelevanzpruefungEingabeFb4Base):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item.")
