from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungEingabeFb3Base(BaseModel):
    """Required (non-nullable) fields"""

    c1q1: int
    c2q1: int


class KlimarelevanzpruefungEingabeFb3Optional(BaseModel):
    """Optional (nullable) fields"""

    # Teil 1
    c1q2: Optional[int] = None
    c1q3: Optional[str] = None
    c1q4: Optional[str] = None  # nullable=True, even if FK defined
    c1q5: Optional[str] = None
    c1q6: Optional[int] = None
    c1q7: Optional[str] = None
    c1q8: Optional[int] = None
    c1q9: Optional[str] = None

    # Teil 2
    c2q2: Optional[int] = None
    c2q3: Optional[str] = None
    c2q4: Optional[int] = None
    c2q5: Optional[str] = None
    c2q6: Optional[int] = None
    c2q7: Optional[str] = None
    c2q8: Optional[int] = None
    c2q9: Optional[str] = None


class KlimarelevanzpruefungEingabeFb3Create(
    KlimarelevanzpruefungEingabeFb3Base, KlimarelevanzpruefungEingabeFb3Optional
):
    """Schema for creating new entries"""

    pass


class KlimarelevanzpruefungEingabeFb3Update(KlimarelevanzpruefungEingabeFb3Optional):
    """Schema for updating entries (all fields optional)"""

    c1q1: Optional[int] = None
    c2q1: Optional[int] = None


class KlimarelevanzpruefungEingabeFb3Read(
    KlimarelevanzpruefungEingabeFb3Base, KlimarelevanzpruefungEingabeFb3Optional
):
    """Schema for reading entries"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item")
