from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimarelevanzpruefungEingabe(Base):
    __tablename__ = "klimarelevanzpruefung_eingabe"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindeeinehit ID",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name der Gemeindeeinheit"
    )
    f1: Mapped[bool] = mapped_column(nullable=False, comment="Fragebogen 1 notwendig")
    fb1_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("klimarelevanzpruefung_eingabe_fb1.id", ondelete="SET NULL"),
        nullable=True,
        comment="Verknüpfung zum Mobilitätscheck Eingabe, falls Fragebogen 1 notwendig ist",
    )
    fb1: Mapped[Optional["KlimarelevanzpruefungEingabeFb1"]] = relationship(
        lazy="selectin"
    )
    f2: Mapped[bool] = mapped_column(nullable=False, comment="Fragebogen 2 notwendig")
    fb2_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("klimarelevanzpruefung_eingabe_fb2.id", ondelete="SET NULL"),
        nullable=True,
        comment="Verknüpfung zum Mobilitätscheck Eingabe, falls Fragebogen 2 notwendig ist",
    )
    fb2: Mapped[Optional["KlimarelevanzpruefungEingabeFb2"]] = relationship(
        lazy="selectin"
    )
    f3: Mapped[bool] = mapped_column(nullable=False, comment="Fragebogen 3 notwendig")
    fb3_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("klimarelevanzpruefung_eingabe_fb3.id", ondelete="SET NULL"),
        nullable=True,
        comment="Verknüpfung zum Mobilitätscheck Eingabe, falls Fragebogen 3 notwendig ist",
    )
    fb3: Mapped[Optional["KlimarelevanzpruefungEingabeFb3"]] = relationship(
        lazy="selectin"
    )
    f4: Mapped[bool] = mapped_column(nullable=False, comment="Fragebogen 4 notwendig")
    fb4_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("klimarelevanzpruefung_eingabe_fb4.id", ondelete="SET NULL"),
        nullable=True,
        comment="Verknüpfung zum Mobilitätscheck Eingabe, falls Fragebogen 4 notwendig ist",
    )
    fb4: Mapped[Optional["KlimarelevanzpruefungEingabeFb4"]] = relationship(
        lazy="selectin"
    )
    f5: Mapped[bool] = mapped_column(nullable=False, comment="Fragebogen 5 notwendig")
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID mit der die Einheit verknüpft ist",
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
from app.models.klimarelevanzpruefung_eingabe_fb1 import KlimarelevanzpruefungEingabeFb1
from app.models.klimarelevanzpruefung_eingabe_fb2 import KlimarelevanzpruefungEingabeFb2
from app.models.klimarelevanzpruefung_eingabe_fb3 import KlimarelevanzpruefungEingabeFb3
from app.models.klimarelevanzpruefung_eingabe_fb4 import KlimarelevanzpruefungEingabeFb4
from app.models.user import User
