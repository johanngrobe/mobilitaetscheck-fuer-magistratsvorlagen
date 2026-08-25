from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class EmailVorlage(Base):
    __tablename__ = "email_vorlage"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Email-Vorlage ID",
    )
    key: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
        comment="Eindeutiger Schlüssel der Vorlage (z.B. 'einladung')",
    )
    betreff: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Betreff der E-Mail. Leer = Standardwert wird verwendet."
    )
    inhalt: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        comment="HTML-Inhalt der E-Mail (Platzhalter wie {{ vorname }} möglich). Leer = Standardvorlage wird verwendet.",
    )
