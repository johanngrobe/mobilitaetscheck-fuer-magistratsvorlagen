"""add nutzungsbedingungen fields

Revision ID: f1a2b3c4d5e6
Revises: de75c362faae
Create Date: 2026-08-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = 'de75c362faae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'nutzungsbedingungen_modus',
            sa.String(),
            nullable=False,
            server_default='inhalt',
            comment="Wie die Nutzungsbedingungen bereitgestellt werden: 'inhalt' (HTML) oder 'url' (externer Link)",
        ),
    )
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'nutzungsbedingungen_inhalt',
            sa.Text(),
            nullable=True,
            comment="Nutzungsbedingungen (HTML), falls nutzungsbedingungen_modus='inhalt'",
        ),
    )
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'nutzungsbedingungen_url',
            sa.String(),
            nullable=True,
            comment="Externe URL der Nutzungsbedingungen, falls nutzungsbedingungen_modus='url'",
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'nutzungsbedingungen_url')
    op.drop_column('plattform_einstellung', 'nutzungsbedingungen_inhalt')
    op.drop_column('plattform_einstellung', 'nutzungsbedingungen_modus')
