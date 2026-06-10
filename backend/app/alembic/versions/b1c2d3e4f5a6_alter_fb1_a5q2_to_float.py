"""alter fb1 a5q2 to float

Revision ID: b1c2d3e4f5a6
Revises: a9f3e1b2c7d8
Create Date: 2026-06-10 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, None] = "a9f3e1b2c7d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    # NULL out any values that cannot be cast to float
    connection.execute(
        sa.text(
            """
        UPDATE klimarelevanzpruefung_eingabe_fb1
        SET a5q2 = NULL
        WHERE a5q2 IS NOT NULL
          AND a5q2 !~ '^-?[0-9]+(\\.[0-9]+)?([eE][+-]?[0-9]+)?$';
        """
        )
    )
    op.alter_column(
        "klimarelevanzpruefung_eingabe_fb1",
        "a5q2",
        existing_type=sa.String(),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using="a5q2::double precision",
    )


def downgrade() -> None:
    op.alter_column(
        "klimarelevanzpruefung_eingabe_fb1",
        "a5q2",
        existing_type=sa.Float(),
        type_=sa.String(),
        existing_nullable=True,
    )
