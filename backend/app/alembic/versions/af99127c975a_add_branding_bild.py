"""add branding_bild table for admin-editable logos and favicon

Revision ID: af99127c975a
Revises: 18a8fef19437
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af99127c975a'
down_revision: Union[str, None] = '18a8fef19437'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'branding_bild',
        sa.Column('id', sa.Integer(), nullable=False, comment='Branding-Bild ID'),
        sa.Column(
            'slot',
            sa.String(),
            nullable=False,
            comment="Eindeutiger Slot-Schlüssel (z.B. 'favicon', 'menue-logo')",
        ),
        sa.Column(
            'dateiname',
            sa.String(),
            nullable=False,
            comment='Gespeicherter Dateiname auf dem Server',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('slot'),
    )
    op.create_index(op.f('ix_branding_bild_slot'), 'branding_bild', ['slot'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_branding_bild_slot'), table_name='branding_bild')
    op.drop_table('branding_bild')
