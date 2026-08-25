"""generalize footer_logo into a bereich-scoped logo_liste_eintrag table and free the login logos

Revision ID: 0a1a88046737
Revises: 50e97021b677
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a1a88046737'
down_revision: Union[str, None] = '50e97021b677'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

OLD_LOGIN_SLOTS = ['login-logo-1', 'login-logo-2', 'login-logo-3']


def upgrade() -> None:
    op.create_table(
        'logo_liste_eintrag',
        sa.Column('id', sa.Integer(), nullable=False, comment='Logo-Listeneintrag ID'),
        sa.Column(
            'bereich',
            sa.String(),
            nullable=False,
            comment="Seitenbereich der Logo-Liste (z.B. 'footer', 'login')",
        ),
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
            comment='Anzeigereihenfolge innerhalb des Bereichs (aufsteigend)',
        ),
        sa.ForeignKeyConstraint(['asset_id'], ['branding_asset.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )
    op.create_index(
        op.f('ix_logo_liste_eintrag_bereich'), 'logo_liste_eintrag', ['bereich'], unique=False
    )

    conn = op.get_bind()

    if sa.inspect(conn).has_table('footer_logo'):
        rows = conn.execute(sa.text('SELECT asset_id, link, reihenfolge FROM footer_logo')).fetchall()
        for asset_id, link, reihenfolge in rows:
            conn.execute(
                sa.text(
                    'INSERT INTO logo_liste_eintrag (bereich, asset_id, link, reihenfolge) '
                    "VALUES ('footer', :asset_id, :link, :reihenfolge)"
                ),
                {'asset_id': asset_id, 'link': link, 'reihenfolge': reihenfolge},
            )
        op.drop_table('footer_logo')

    if sa.inspect(conn).has_table('branding_slot_zuweisung'):
        rows = conn.execute(
            sa.text(
                'SELECT slot, asset_id FROM branding_slot_zuweisung '
                'WHERE slot = ANY(:slots) AND asset_id IS NOT NULL ORDER BY slot'
            ),
            {'slots': OLD_LOGIN_SLOTS},
        ).fetchall()
        for position, (slot, asset_id) in enumerate(rows):
            conn.execute(
                sa.text(
                    'INSERT INTO logo_liste_eintrag (bereich, asset_id, reihenfolge) '
                    "VALUES ('login', :asset_id, :reihenfolge)"
                ),
                {'asset_id': asset_id, 'reihenfolge': position},
            )
        conn.execute(
            sa.text('DELETE FROM branding_slot_zuweisung WHERE slot = ANY(:slots)'),
            {'slots': OLD_LOGIN_SLOTS},
        )


def downgrade() -> None:
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
    rows = conn.execute(
        sa.text(
            "SELECT asset_id, link, reihenfolge FROM logo_liste_eintrag WHERE bereich = 'footer'"
        )
    ).fetchall()
    for asset_id, link, reihenfolge in rows:
        conn.execute(
            sa.text(
                'INSERT INTO footer_logo (asset_id, link, reihenfolge) '
                'VALUES (:asset_id, :link, :reihenfolge)'
            ),
            {'asset_id': asset_id, 'link': link, 'reihenfolge': reihenfolge},
        )

    op.drop_index(op.f('ix_logo_liste_eintrag_bereich'), table_name='logo_liste_eintrag')
    op.drop_table('logo_liste_eintrag')
