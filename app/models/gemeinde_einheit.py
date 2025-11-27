from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class GemeindeEinheit(Base):
    __tablename__ = "gemeinde_einheit"

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
    rolle_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_rolle.id", ondelete="SET NULL"),
        nullable=True,
        comment="Rollen ID der Gemeindeeinheit",
    )
    rolle: Mapped[Optional["UserRolle"]] = relationship(
        back_populates="gemeinde_einheiten", lazy="selectin"
    )
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID mit der die Einheit verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(
        back_populates="einheiten", lazy="selectin"
    )


from app.models.gemeinde import Gemeinde
from app.models.user_rolle import UserRolle
