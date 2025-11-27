from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.assoziation_klimarelevanzpruefung_vorhaben_energiestandard import (
    klimarelevanzpruefung_vorhaben_energiestandard_assoziation,
)


class KlimarelevanzpruefungVorhaben(Base):
    __tablename__ = "klimarelevanzpruefung_vorhaben"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID",
    )
    name: Mapped[str] = mapped_column(nullable=False, comment="Name des Bauvorhabens")

    energiestandards: Mapped[Optional[List["KlimarelevanzpruefungEnergiestandard"]]] = (
        relationship(
            secondary=klimarelevanzpruefung_vorhaben_energiestandard_assoziation,
            cascade="all, delete",
            lazy="selectin",
        )
    )


from app.models.klimarelevanzpruefung_energiestandard import (
    KlimarelevanzpruefungEnergiestandard,
)
