from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimarelevanzpruefungEingabeFb1(Base):
    __tablename__ = "klimarelevanzpruefung_eingabe_fb1"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindeeinehit ID",
    )
    a1q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 1 Frage 1",
    )
    a1q2: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 2")
    a1q3: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 3",
    )
    a1q4: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 4")
    a1q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 5")
    a2q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 2 Frage 1",
    )
    a2q2: Mapped[Optional[int]] = mapped_column(
        ForeignKey("klimarelevanzpruefung_vorhaben.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 2",
    )
    a2q3: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 3",
    )
    a2q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("klimarelevanzpruefung_energiestandard.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 4",
    )
    a2q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 5")
    a2q6: Mapped[Optional[int]] = mapped_column(
        ForeignKey("klimarelevanzpruefung_energiestandard.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 6",
    )
    a2q7: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 7")
    a2q8: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 8",
    )
    a2q9: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 9")
    a2q10: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 10",
    )
    a2q11: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 2 Frage 11"
    )
    a2q12: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 12",
    )
    a2q13: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 2 Frage 13"
    )
    a2q14: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 14",
    )
    a2q15: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 2 Frage 15"
    )
    a3q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 3 Frage 1",
    )
    a3q2: Mapped[Optional[float]] = mapped_column(
        nullable=True, comment="Teil 3 Frage 2"
    )
    a3q3: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 3 Frage 3")
    a3q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 3 Frage 4",
    )
    a3q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 3 Frage 3")
    a3q6: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 3 Frage 4")
    a4q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 4 Frage 1",
    )
    a4q2: Mapped[Optional[float]] = mapped_column(
        nullable=True, comment="Teil 4 Frage 2"
    )
    a4q3: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 4 Frage 3")
    a4q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 4 Frage 4",
    )
    a5q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 5 Frage 1",
    )
    a5q2: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 5 Frage 2")
    a5q3: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 5 Frage 3")
    a5q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 5 Frage 4",
    )
    a6q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 6 Frage 1",
    )
    a6q2: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 6 Frage 2")
    a6q3: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 6 Frage 3",
    )
    a6q4: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 6 Frage 4")
    a6q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 6 Frage 5")
    a7q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 7 Frage 1",
    )
    a7q2: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 7 Frage 2")
    a8q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 7 Frage 1",
    )
    a8q2: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 7 Frage 2")

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
