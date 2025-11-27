from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungEingabeBase(BaseModel):

    name: str = Field(..., description="The name of the Gemeinde.")
    f1: bool = Field(..., description="Fb1")
    f2: bool = Field(..., description="Fb2")
    f3: bool = Field(..., description="Fb3")
    f4: bool = Field(..., description="Fb4")
    f5: bool = Field(..., description="Fb5")
    fb1_id: Optional[int] = Field(None, description="Foreign key to FB1 input.")
    fb2_id: Optional[int] = Field(None, description="Foreign key to FB2 input.")
    fb3_id: Optional[int] = Field(None, description="Foreign key to FB3 input.")
    fb4_id: Optional[int] = Field(None, description="Foreign key to FB4 input.")


class KlimarelevanzpruefungEingabeCreate(KlimarelevanzpruefungEingabeBase):
    pass


class KlimarelevanzpruefungEingabeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Aktualisierter Name des Items")
    f1: Optional[bool] = Field(False, description="Fb1")
    f2: Optional[bool] = Field(False, description="Fb2")
    f3: Optional[bool] = Field(False, description="Fb3")
    f4: Optional[bool] = Field(False, description="Fb4")
    f5: Optional[bool] = Field(False, description="Fb5")
    fb1_id: Optional[int] = Field(None, description="Foreign key to FB1 input.")
    fb2_id: Optional[int] = Field(None, description="Foreign key to FB2 input.")
    fb3_id: Optional[int] = Field(None, description="Foreign key to FB3 input.")
    fb4_id: Optional[int] = Field(None, description="Foreign key to FB4 input.")


class KlimarelevanzpruefungEingabeRead(KlimarelevanzpruefungEingabeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item.")
    fb1: Optional["KlimarelevanzpruefungEingabeFb1Read"] = Field(
        None, description="Associated FB1 input object."
    )
    fb2: Optional["KlimarelevanzpruefungEingabeFb2Read"] = Field(
        None, description="Associated FB2 input object."
    )
    fb3: Optional["KlimarelevanzpruefungEingabeFb3Read"] = Field(
        None, description="Associated FB3 input object."
    )
    fb4: Optional["KlimarelevanzpruefungEingabeFb4Read"] = Field(
        None, description="Associated FB4 input object."
    )


from app.schemas.klimarelevanzpruefung_eingabe_fb1 import (
    KlimarelevanzpruefungEingabeFb1Read,
)
from app.schemas.klimarelevanzpruefung_eingabe_fb2 import (
    KlimarelevanzpruefungEingabeFb2Read,
)
from app.schemas.klimarelevanzpruefung_eingabe_fb3 import (
    KlimarelevanzpruefungEingabeFb3Read,
)
from app.schemas.klimarelevanzpruefung_eingabe_fb4 import (
    KlimarelevanzpruefungEingabeFb4Read,
)
