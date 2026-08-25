"""add startseite_inhalt to plattform_einstellung for admin-editable homepage content

Revision ID: de75c362faae
Revises: 0a1a88046737
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de75c362faae'
down_revision: Union[str, None] = '0a1a88046737'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'startseite_inhalt',
            sa.Text(),
            nullable=True,
            comment='Inhalt (HTML) der Startseite, ersetzt den Standard-Hero-Bereich',
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'startseite_inhalt')
