from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class PlattformEinstellung(Base):
    __tablename__ = "plattform_einstellung"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Plattform-Einstellung ID",
    )
    datenschutzerklaerung: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Datenschutzerklärung (HTML), die bei der Registrierung angezeigt wird"
    )
    datenschutz_modus: Mapped[str] = mapped_column(
        nullable=False,
        default="inhalt",
        server_default="inhalt",
        comment="Wie die Datenschutzerklärung bereitgestellt wird: 'inhalt' (HTML) oder 'url' (externer Link)",
    )
    datenschutz_url: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Externe URL der Datenschutzerklärung, falls datenschutz_modus='url'"
    )
    impressum_modus: Mapped[str] = mapped_column(
        nullable=False,
        default="inhalt",
        server_default="inhalt",
        comment="Wie das Impressum bereitgestellt wird: 'inhalt' (HTML) oder 'url' (externer Link)",
    )
    impressum_inhalt: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Impressum (HTML), falls impressum_modus='inhalt'"
    )
    impressum_url: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Externe URL des Impressums, falls impressum_modus='url'"
    )
    ueber_das_tool_inhalt: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Inhalt (HTML) der Seite 'Über das Tool'"
    )
    startseite_inhalt: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Inhalt (HTML) der Startseite, ersetzt den Standard-Hero-Bereich"
    )
