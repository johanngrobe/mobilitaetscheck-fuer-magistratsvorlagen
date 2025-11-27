from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class KlimarelevanzpruefungEingabeFb1Base(BaseModel):
    """Fields that are required (nullable=False)"""

    # Required bool_erweitert references
    a1q1: int
    a2q1: int
    a3q1: int
    a4q1: int
    a5q1: int
    a6q1: int
    a7q1: int
    a8q1: int


class KlimarelevanzpruefungEingabeFb1Optional(BaseModel):
    """Fields that are optional (nullable=True)"""

    # Teil 1
    a1q2: Optional[str] = None
    a1q3: Optional[int] = None
    a1q4: Optional[str] = None
    a1q5: Optional[str] = None

    # Teil 2
    a2q2: Optional[int] = None
    a2q3: Optional[int] = None
    a2q4: Optional[int] = None
    a2q5: Optional[str] = None
    a2q6: Optional[int] = None
    a2q7: Optional[str] = None
    a2q8: Optional[int] = None
    a2q9: Optional[str] = None
    a2q10: Optional[int] = None
    a2q11: Optional[str] = None
    a2q12: Optional[int] = None
    a2q13: Optional[str] = None
    a2q14: Optional[int] = None
    a2q15: Optional[str] = None

    # Teil 3
    a3q2: Optional[float] = None
    a3q3: Optional[str] = None
    a3q4: Optional[int] = None
    a3q5: Optional[str] = None
    a3q6: Optional[str] = None

    # Teil 4
    a4q2: Optional[float] = None
    a4q3: Optional[str] = None
    a4q4: Optional[int] = None

    # Teil 5
    a5q2: Optional[str] = None
    a5q3: Optional[str] = None
    a5q4: Optional[int] = None

    # Teil 6
    a6q2: Optional[str] = None
    a6q3: Optional[int] = None
    a6q4: Optional[str] = None
    a6q5: Optional[str] = None

    # Teil 7
    a7q2: Optional[str] = None

    # Teil 8
    a8q2: Optional[str] = None


class KlimarelevanzpruefungEingabeFb1Create(
    KlimarelevanzpruefungEingabeFb1Base, KlimarelevanzpruefungEingabeFb1Optional
):
    """Schema for creating new entries"""

    pass


class KlimarelevanzpruefungEingabeFb1Update(KlimarelevanzpruefungEingabeFb1Optional):
    """Schema for updating entries — all fields optional"""

    # Base fields as optional
    a1q1: Optional[int] = None
    a2q1: Optional[int] = None
    a3q1: Optional[int] = None
    a4q1: Optional[int] = None
    a5q1: Optional[int] = None
    a6q1: Optional[int] = None
    a7q1: Optional[int] = None
    a8q1: Optional[int] = None


class KlimarelevanzpruefungEingabeFb1Read(
    KlimarelevanzpruefungEingabeFb1Base, KlimarelevanzpruefungEingabeFb1Optional
):
    """Schema for reading entries"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Kennung für das Item")
