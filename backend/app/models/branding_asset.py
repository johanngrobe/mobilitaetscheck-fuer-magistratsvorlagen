from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.db import Base


class BrandingAsset(Base):
    __tablename__ = "branding_asset"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, nullable=False, unique=True, comment="Branding-Asset ID"
    )
    dateiname: Mapped[str] = mapped_column(
        nullable=False, comment="Gespeicherter Dateiname auf dem Server"
    )
    original_dateiname: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Ursprünglicher Dateiname beim Hochladen"
    )
    erstellt_am: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment="Zeitpunkt des Uploads"
    )
