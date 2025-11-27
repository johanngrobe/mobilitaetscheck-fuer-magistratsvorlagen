from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimarelevanzpruefungEingabeFb4(Base):
    __tablename__ = "klimarelevanzpruefung_eingabe_fb4"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindeeinehit ID",
    )
    d1q1: Mapped[str] = mapped_column(
        nullable=False,
        comment="Teil 1 Frage 1",
    )

    d2q1: Mapped[str] = mapped_column(
        nullable=False,
        comment="Teil 2 Frage 1",
    )

    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(lazy="selectin")
    erstellt_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID des Erstellers",
    )
    autor: Mapped[Optional["User"]] = relationship(
        foreign_keys=[erstellt_von], lazy="selectin"
    )
    zuletzt_bearbeitet_von: Mapped[Optional[GUID]] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="User ID des zuletzt bearbeitenden Benutzers",
    )
    letzter_bearbeiter: Mapped[Optional["User"]] = relationship(
        foreign_keys=[zuletzt_bearbeitet_von], lazy="selectin"
    )


from app.models.gemeinde import Gemeinde
from app.models.user import User
