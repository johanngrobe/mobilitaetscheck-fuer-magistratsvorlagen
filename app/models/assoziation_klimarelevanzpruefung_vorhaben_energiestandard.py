from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between mobility_results and indicators
klimarelevanzpruefung_vorhaben_energiestandard_assoziation = Table(
    "klimarelevanzpruefung_vorhaben_energiestandard",
    Base.metadata,
    Column(
        "vorhaben_id",
        Integer,
        ForeignKey("klimarelevanzpruefung_vorhaben.id", ondelete="CASCADE"),
    ),
    Column(
        "energiestandard_id",
        Integer,
        ForeignKey("klimarelevanzpruefung_energiestandard.id", ondelete="CASCADE"),
    ),
)
