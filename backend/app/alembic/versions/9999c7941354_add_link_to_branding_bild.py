"""add link column to branding_bild for clickable footer logos

Revision ID: 9999c7941354
Revises: af99127c975a
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9999c7941354'
down_revision: Union[str, None] = 'af99127c975a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'branding_bild',
        sa.Column(
            'link',
            sa.String(),
            nullable=True,
            comment='Optionales Link-Ziel, falls das Bild verlinkt werden kann',
        ),
    )


def downgrade() -> None:
    op.drop_column('branding_bild', 'link')
