"""add plattform_einstellung table for datenschutzerklaerung

Revision ID: 94f61d7382fa
Revises: b1c2d3e4f5a6
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94f61d7382fa'
down_revision: Union[str, None] = 'b1c2d3e4f5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'plattform_einstellung',
        sa.Column('id', sa.Integer(), nullable=False, comment='Plattform-Einstellung ID'),
        sa.Column(
            'datenschutzerklaerung',
            sa.Text(),
            nullable=True,
            comment='Datenschutzerklärung (HTML), die bei der Registrierung angezeigt wird',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('plattform_einstellung')
