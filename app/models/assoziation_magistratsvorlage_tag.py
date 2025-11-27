from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db import Base

# association table for many-to-many relationship between mobility_results and indicators
magistratsvorlage_tag_assoziation = Table(
    "magistratsvorlage_tag",
    Base.metadata,
    Column(
        "tag_id",
        Integer,
        ForeignKey("tag.id", ondelete="CASCADE"),
    ),
    Column(
        "magistratsvorlage_id",
        Integer,
        ForeignKey("magistratsvorlage.id", ondelete="CASCADE"),
    ),
)
