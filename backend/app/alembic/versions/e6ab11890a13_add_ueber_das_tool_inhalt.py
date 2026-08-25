"""add ueber_das_tool_inhalt to plattform_einstellung for admin-editable page content

Revision ID: e6ab11890a13
Revises: 9999c7941354
Create Date: 2026-08-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6ab11890a13'
down_revision: Union[str, None] = '9999c7941354'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'ueber_das_tool_inhalt',
            sa.Text(),
            nullable=True,
            comment="Inhalt (HTML) der Seite 'Über das Tool'",
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'ueber_das_tool_inhalt')
