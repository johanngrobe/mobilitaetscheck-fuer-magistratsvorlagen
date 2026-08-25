"""turn footer logos into a flexible ordered list instead of 4 fixed slots

Revision ID: 50e97021b677
Revises: ab6e6a34a2d5
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50e97021b677'
down_revision: Union[str, None] = 'ab6e6a34a2d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

OLD_FOOTER_SLOTS = ['footer-logo-1', 'footer-logo-2', 'footer-logo-3', 'footer-logo-4']


def upgrade() -> None:
    op.create_table(
        'footer_logo',
        sa.Column('id', sa.Integer(), nullable=False, comment='Footer-Logo ID'),
        sa.Column('asset_id', sa.Integer(), nullable=False, comment='Zugewiesenes Branding-Asset'),
        sa.Column(
            'link',
            sa.String(),
            nullable=True,
            comment='Optionales Link-Ziel, das beim Klick auf das Logo geöffnet wird',
        ),
        sa.Column(
            'reihenfolge',
            sa.Integer(),
            nullable=False,
            server_default='0',
            comment='Anzeigereihenfolge im Footer (aufsteigend)',
        ),
        sa.ForeignKeyConstraint(['asset_id'], ['branding_asset.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )

    conn = op.get_bind()
    if sa.inspect(conn).has_table('branding_slot_zuweisung'):
        rows = conn.execute(
            sa.text(
                'SELECT slot, asset_id, link FROM branding_slot_zuweisung '
                'WHERE slot = ANY(:slots) AND asset_id IS NOT NULL ORDER BY slot'
            ),
            {'slots': OLD_FOOTER_SLOTS},
        ).fetchall()
        for position, (slot, asset_id, link) in enumerate(rows):
            conn.execute(
                sa.text(
                    'INSERT INTO footer_logo (asset_id, link, reihenfolge) '
                    'VALUES (:asset_id, :link, :reihenfolge)'
                ),
                {'asset_id': asset_id, 'link': link, 'reihenfolge': position},
            )
        conn.execute(
            sa.text('DELETE FROM branding_slot_zuweisung WHERE slot = ANY(:slots)'),
            {'slots': OLD_FOOTER_SLOTS},
        )


def downgrade() -> None:
    op.drop_table('footer_logo')
