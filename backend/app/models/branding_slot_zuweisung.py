from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class BrandingSlotZuweisung(Base):
    __tablename__ = "branding_slot_zuweisung"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Branding-Slot-Zuweisung ID",
    )
    slot: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
        comment="Eindeutiger Slot-Schlüssel (z.B. 'favicon', 'menue-logo')",
    )
    asset_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("branding_asset.id", ondelete="SET NULL"),
        nullable=True,
        comment="Zugewiesenes Branding-Asset für diesen Slot",
    )
    link: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Optionales Link-Ziel, falls das Bild verlinkt werden kann"
    )

    asset: Mapped[Optional["BrandingAsset"]] = relationship(lazy="selectin")
