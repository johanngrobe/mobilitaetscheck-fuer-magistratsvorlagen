from typing import Optional, List

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class BoolErweitert(Base):
    __tablename__ = "bool_erweitert"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="ID",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name der Gemeindeeinheit"
    )
