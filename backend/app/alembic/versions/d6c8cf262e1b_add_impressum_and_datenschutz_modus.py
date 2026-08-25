"""add impressum fields and url-mode toggle for impressum/datenschutz

Revision ID: d6c8cf262e1b
Revises: e6ab11890a13
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6c8cf262e1b'
down_revision: Union[str, None] = 'e6ab11890a13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'datenschutz_modus',
            sa.String(),
            nullable=False,
            server_default='inhalt',
            comment="Wie die Datenschutzerklärung bereitgestellt wird: 'inhalt' (HTML) oder 'url' (externer Link)",
        ),
    )
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'datenschutz_url',
            sa.String(),
            nullable=True,
            comment="Externe URL der Datenschutzerklärung, falls datenschutz_modus='url'",
        ),
    )
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'impressum_modus',
            sa.String(),
            nullable=False,
            server_default='inhalt',
            comment="Wie das Impressum bereitgestellt wird: 'inhalt' (HTML) oder 'url' (externer Link)",
        ),
    )
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'impressum_inhalt',
            sa.Text(),
            nullable=True,
            comment="Impressum (HTML), falls impressum_modus='inhalt'",
        ),
    )
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'impressum_url',
            sa.String(),
            nullable=True,
            comment="Externe URL des Impressums, falls impressum_modus='url'",
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'impressum_url')
    op.drop_column('plattform_einstellung', 'impressum_inhalt')
    op.drop_column('plattform_einstellung', 'impressum_modus')
    op.drop_column('plattform_einstellung', 'datenschutz_url')
    op.drop_column('plattform_einstellung', 'datenschutz_modus')
