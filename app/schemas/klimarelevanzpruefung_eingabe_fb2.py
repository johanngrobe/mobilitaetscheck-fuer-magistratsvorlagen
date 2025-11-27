from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungEingabeFb2Base(BaseModel):
    """Required (non-nullable) fields"""

    b1q1: int
    a2q1: int


class KlimarelevanzpruefungEingabeFb2Optional(BaseModel):
    """Optional (nullable) fields"""

    # Teil 1
    b1q2: Optional[int] = None
    b1q3: Optional[str] = None
    b1q4: Optional[int] = None
    b1q5: Optional[str] = None
    b1q6: Optional[int] = None
    b1q7: Optional[str] = None
    b1q8: Optional[str] = None
    b1q9: Optional[int] = None
    b1q10: Optional[str] = None
    b1q11: Optional[str] = None
    b1q12: Optional[int] = None
    b1q13: Optional[str] = None
    b1q14: Optional[str] = None
    b1q15: Optional[int] = None
    b1q16: Optional[str] = None
    b1q17: Optional[str] = None
    b1q18: Optional[int] = None
    b1q19: Optional[str] = None
    b1q20: Optional[str] = None

    # Teil 2
    a2q2: Optional[str] = None
    a2q3: Optional[str] = None
    a2q4: Optional[int] = None
    a2q5: Optional[str] = None


class KlimarelevanzpruefungEingabeFb2Create(
    KlimarelevanzpruefungEingabeFb2Base, KlimarelevanzpruefungEingabeFb2Optional
):
    """Schema for creating new entries"""

    pass


class KlimarelevanzpruefungEingabeFb2Update(KlimarelevanzpruefungEingabeFb2Optional):
    """Schema for updating entries (all fields optional)"""

    b1q1: Optional[int] = None
    a2q1: Optional[int] = None


class KlimarelevanzpruefungEingabeFb2Read(
    KlimarelevanzpruefungEingabeFb2Base, KlimarelevanzpruefungEingabeFb2Optional
):
    """Schema for reading entries"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item")
