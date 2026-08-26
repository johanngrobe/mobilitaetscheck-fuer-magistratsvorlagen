from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

RechtstextModus = Literal["inhalt", "url"]


class PlattformEinstellungBase(BaseModel):
    datenschutzerklaerung: Optional[str] = Field(
        None, description="Datenschutzerklärung (HTML), die bei der Registrierung angezeigt wird."
    )
    datenschutz_modus: RechtstextModus = Field(
        "inhalt", description="Wie die Datenschutzerklärung bereitgestellt wird."
    )
    datenschutz_url: Optional[str] = Field(
        None, description="Externe URL der Datenschutzerklärung, falls datenschutz_modus='url'."
    )
    impressum_modus: RechtstextModus = Field(
        "inhalt", description="Wie das Impressum bereitgestellt wird."
    )
    impressum_inhalt: Optional[str] = Field(
        None, description="Impressum (HTML), falls impressum_modus='inhalt'."
    )
    impressum_url: Optional[str] = Field(
        None, description="Externe URL des Impressums, falls impressum_modus='url'."
    )
    nutzungsbedingungen_modus: RechtstextModus = Field(
        "inhalt", description="Wie die Nutzungsbedingungen bereitgestellt werden."
    )
    nutzungsbedingungen_inhalt: Optional[str] = Field(
        None, description="Nutzungsbedingungen (HTML), falls nutzungsbedingungen_modus='inhalt'."
    )
    nutzungsbedingungen_url: Optional[str] = Field(
        None, description="Externe URL der Nutzungsbedingungen, falls nutzungsbedingungen_modus='url'."
    )
    ueber_das_tool_inhalt: Optional[str] = Field(
        None, description="Inhalt (HTML) der Seite 'Über das Tool'."
    )
    startseite_inhalt: Optional[str] = Field(
        None, description="Inhalt (HTML) der Startseite, ersetzt den Standard-Hero-Bereich."
    )


class PlattformEinstellungUpdate(PlattformEinstellungBase):
    datenschutz_modus: Optional[RechtstextModus] = Field(None)
    impressum_modus: Optional[RechtstextModus] = Field(None)
    nutzungsbedingungen_modus: Optional[RechtstextModus] = Field(None)


class PlattformEinstellungRead(PlattformEinstellungBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the Plattform-Einstellung.")
