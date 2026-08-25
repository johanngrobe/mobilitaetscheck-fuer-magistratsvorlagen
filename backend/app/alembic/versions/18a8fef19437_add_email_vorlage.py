"""add email_vorlage table for admin-editable email templates

Revision ID: 18a8fef19437
Revises: 94f61d7382fa
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18a8fef19437'
down_revision: Union[str, None] = '94f61d7382fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'email_vorlage',
        sa.Column('id', sa.Integer(), nullable=False, comment='Email-Vorlage ID'),
        sa.Column(
            'key',
            sa.String(),
            nullable=False,
            comment="Eindeutiger Schlüssel der Vorlage (z.B. 'einladung')",
        ),
        sa.Column(
            'betreff',
            sa.String(),
            nullable=True,
            comment='Betreff der E-Mail. Leer = Standardwert wird verwendet.',
        ),
        sa.Column(
            'inhalt',
            sa.Text(),
            nullable=True,
            comment='HTML-Inhalt der E-Mail (Platzhalter wie {{ vorname }} möglich). Leer = Standardvorlage wird verwendet.',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('key'),
    )
    op.create_index(op.f('ix_email_vorlage_key'), 'email_vorlage', ['key'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_email_vorlage_key'), table_name='email_vorlage')
    op.drop_table('email_vorlage')
