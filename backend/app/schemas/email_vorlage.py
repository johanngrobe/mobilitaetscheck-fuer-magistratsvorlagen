from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class EmailVorlageBase(BaseModel):
    betreff: Optional[str] = Field(None, description="Betreff der E-Mail.")
    inhalt: Optional[str] = Field(None, description="HTML-Inhalt der E-Mail.")


class EmailVorlageUpdate(EmailVorlageBase):
    pass


class EmailVorlageRead(EmailVorlageBase):
    model_config = ConfigDict(from_attributes=True)

    key: str = Field(..., description="Eindeutiger Schlüssel der Vorlage.")
    standard_betreff: str = Field(..., description="Standard-Betreff, falls kein eigener gesetzt ist.")
    standard_inhalt: str = Field(..., description="Standard-Inhalt, falls kein eigener gesetzt ist.")
    platzhalter: list[str] = Field(..., description="In dieser Vorlage verfügbare Platzhalter.")
