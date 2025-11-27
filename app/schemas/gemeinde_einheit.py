from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GemeindeEinheitBase(BaseModel):

    name: str = Field(..., description="The name of the Gemeinde.")
    rolle_id: int = Field(..., description="ID of the associated Rolle")


class GemeindeEinheitCreate(GemeindeEinheitBase):
    pass


class GemeindeEinheitUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Aktualisierter Name des Items")
    rolle_id: Optional[int] = Field(
        None, description="Aktualisierte ID der zugehörigen Rolle"
    )


class GemeindeEinheitRead(GemeindeEinheitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item.")
    rolle: Optional["UserRolle"] = Field(None, description="Associated Rolle object.")
    gemeinde_id: int = Field(..., description="ID of the associated Gemeinde.")
    gemeinde: Optional["GemeindeRead"] = Field(
        None, description="Associated Gemeinde object."
    )


from app.schemas.gemeinde import GemeindeRead
from app.schemas.user_rolle import UserRolle
