from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BoolErweitertBase(BaseModel):

    name: str = Field(..., description="The name of the Gemeinde.")


class BoolErweitertCreate(BoolErweitertBase):
    pass


class BoolErweitertUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Aktualisierter Name des Items")


class BoolErweitertRead(BoolErweitertBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item.")
