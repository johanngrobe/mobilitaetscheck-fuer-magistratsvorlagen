from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KlimarelevanzpruefungEingabeFb2(Base):
    __tablename__ = "klimarelevanzpruefung_eingabe_fb2"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeindeeinehit ID",
    )
    b1q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 1 Frage 1",
    )
    b1q2: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 2",
    )
    b1q3: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 1 Frage 3",
    )
    b1q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 4",
    )
    b1q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 5")
    b1q6: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 6",
    )
    b1q7: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 7")
    b1q8: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 1 Frage 8")
    b1q9: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 9",
    )
    b1q10: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 10"
    )
    b1q11: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 11"
    )
    b1q12: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 12",
    )
    b1q13: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 13"
    )
    b1q14: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 14"
    )
    b1q15: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 15",
    )
    b1q16: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 16"
    )
    b1q17: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 17"
    )
    b1q18: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 1 Frage 18",
    )
    b1q19: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 19"
    )
    b1q20: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Teil 1 Frage 20"
    )

    a2q1: Mapped[int] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=False,
        comment="Teil 2 Frage 1",
    )
    a2q2: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 2 Frage 2",
    )
    a2q3: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="Teil 2 Frage 3",
    )
    a2q4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bool_erweitert.id", ondelete="SET NULL"),
        nullable=True,
        comment="Teil 2 Frage 4",
    )
    a2q5: Mapped[Optional[str]] = mapped_column(nullable=True, comment="Teil 2 Frage 5")

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
