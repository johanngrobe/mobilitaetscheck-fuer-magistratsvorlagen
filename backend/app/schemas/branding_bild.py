from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BrandingAssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Eindeutige ID des Assets.")
    url: str = Field(..., description="URL des Bildes.")
    original_dateiname: Optional[str] = Field(None, description="Ursprünglicher Dateiname.")
    erstellt_am: datetime = Field(..., description="Zeitpunkt des Uploads.")
    in_verwendung: bool = Field(..., description="Gibt an, ob das Asset aktuell einem Slot zugewiesen ist.")


class BrandingSlotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slot: str = Field(..., description="Eindeutiger Slot-Schlüssel.")
    label: str = Field(..., description="Anzeigename des Slots.")
    beschreibung: str = Field(..., description="Beschreibung, wo das Bild verwendet wird.")
    bereich: str = Field(..., description="Seitenbereich, dem der Slot zugeordnet ist.")
    asset: Optional[BrandingAssetRead] = Field(None, description="Aktuell zugewiesenes Asset, falls vorhanden.")
    verlinkbar: bool = Field(..., description="Gibt an, ob für diesen Slot ein Link hinterlegt werden kann.")
    link: Optional[str] = Field(None, description="Link-Ziel, das beim Klick auf das Bild geöffnet wird.")


class BrandingSlotAssignUpdate(BaseModel):
    asset_id: Optional[int] = Field(None, description="ID des zuzuweisenden Assets, oder null um zu entfernen.")


class BrandingBildLinkUpdate(BaseModel):
    link: Optional[str] = Field(None, description="Link-Ziel, das beim Klick auf das Bild geöffnet wird.")


class LogoListeEintragRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Eindeutige ID des Logo-Listeneintrags.")
    bereich: str = Field(..., description="Seitenbereich der Logo-Liste.")
    asset: BrandingAssetRead = Field(..., description="Zugewiesenes Asset.")
    link: Optional[str] = Field(None, description="Link-Ziel, das beim Klick auf das Logo geöffnet wird.")
    reihenfolge: int = Field(..., description="Anzeigereihenfolge innerhalb des Bereichs.")


class LogoListeEintragCreate(BaseModel):
    asset_id: int = Field(..., description="ID des zuzuweisenden Assets.")
    link: Optional[str] = Field(None, description="Link-Ziel, das beim Klick auf das Logo geöffnet wird.")


class LogoListeEintragUpdate(BaseModel):
    link: Optional[str] = Field(None, description="Link-Ziel, das beim Klick auf das Logo geöffnet wird.")


class LogoListeReorderItem(BaseModel):
    id: int = Field(..., description="ID des Logo-Listeneintrags.")
    reihenfolge: int = Field(..., description="Neue Anzeigereihenfolge.")


class LogoListeReorderUpdate(BaseModel):
    reihenfolge: list[LogoListeReorderItem] = Field(..., description="Neue Reihenfolge aller Einträge.")
