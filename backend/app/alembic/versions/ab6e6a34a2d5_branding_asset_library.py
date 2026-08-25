"""restructure branding into a shared asset library with per-slot assignments

Revision ID: ab6e6a34a2d5
Revises: d6c8cf262e1b
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab6e6a34a2d5'
down_revision: Union[str, None] = 'd6c8cf262e1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'branding_asset',
        sa.Column('id', sa.Integer(), nullable=False, comment='Branding-Asset ID'),
        sa.Column('dateiname', sa.String(), nullable=False, comment='Gespeicherter Dateiname auf dem Server'),
        sa.Column(
            'original_dateiname',
            sa.String(),
            nullable=True,
            comment='Ursprünglicher Dateiname beim Hochladen',
        ),
        sa.Column(
            'erstellt_am',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
            comment='Zeitpunkt des Uploads',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )

    op.create_table(
        'branding_slot_zuweisung',
        sa.Column('id', sa.Integer(), nullable=False, comment='Branding-Slot-Zuweisung ID'),
        sa.Column(
            'slot',
            sa.String(),
            nullable=False,
            comment="Eindeutiger Slot-Schlüssel (z.B. 'favicon', 'menue-logo')",
        ),
        sa.Column('asset_id', sa.Integer(), nullable=True, comment='Zugewiesenes Branding-Asset für diesen Slot'),
        sa.Column(
            'link',
            sa.String(),
            nullable=True,
            comment='Optionales Link-Ziel, falls das Bild verlinkt werden kann',
        ),
        sa.ForeignKeyConstraint(['asset_id'], ['branding_asset.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('slot'),
    )
    op.create_index(
        op.f('ix_branding_slot_zuweisung_slot'), 'branding_slot_zuweisung', ['slot'], unique=True
    )

    conn = op.get_bind()
    if sa.inspect(conn).has_table('branding_bild'):
        rows = conn.execute(sa.text('SELECT slot, dateiname, link FROM branding_bild')).fetchall()
        for slot, dateiname, link in rows:
            asset_id = None
            if dateiname:
                result = conn.execute(
                    sa.text(
                        'INSERT INTO branding_asset (dateiname, original_dateiname) '
                        'VALUES (:dateiname, :dateiname) RETURNING id'
                    ),
                    {'dateiname': dateiname},
                )
                asset_id = result.scalar_one()
            conn.execute(
                sa.text(
                    'INSERT INTO branding_slot_zuweisung (slot, asset_id, link) '
                    'VALUES (:slot, :asset_id, :link)'
                ),
                {'slot': slot, 'asset_id': asset_id, 'link': link},
            )
        op.drop_table('branding_bild')


def downgrade() -> None:
    op.create_table(
        'branding_bild',
        sa.Column('id', sa.Integer(), nullable=False, comment='Branding-Bild ID'),
        sa.Column(
            'slot',
            sa.String(),
            nullable=False,
            comment="Eindeutiger Slot-Schlüssel (z.B. 'favicon', 'menue-logo')",
        ),
        sa.Column('dateiname', sa.String(), nullable=False, comment='Gespeicherter Dateiname auf dem Server'),
        sa.Column(
            'link',
            sa.String(),
            nullable=True,
            comment='Optionales Link-Ziel, falls das Bild verlinkt werden kann',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('slot'),
    )
    op.create_index(op.f('ix_branding_bild_slot'), 'branding_bild', ['slot'], unique=True)

    conn = op.get_bind()
    rows = conn.execute(
        sa.text(
            'SELECT z.slot, a.dateiname, z.link FROM branding_slot_zuweisung z '
            'LEFT JOIN branding_asset a ON a.id = z.asset_id'
        )
    ).fetchall()
    for slot, dateiname, link in rows:
        conn.execute(
            sa.text(
                'INSERT INTO branding_bild (slot, dateiname, link) VALUES (:slot, :dateiname, :link)'
            ),
            {'slot': slot, 'dateiname': dateiname or '', 'link': link},
        )

    op.drop_table('branding_slot_zuweisung')
    op.drop_table('branding_asset')
