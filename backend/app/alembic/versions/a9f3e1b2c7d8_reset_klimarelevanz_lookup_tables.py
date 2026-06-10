"""reset klimarelevanz lookup tables

Revision ID: a9f3e1b2c7d8
Revises: f37510ecaac5
Create Date: 2026-06-10 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a9f3e1b2c7d8"
down_revision: Union[str, None] = "f37510ecaac5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    # --- klimarelevanzpruefung_vorhaben ---
    # Rename existing entries to include " (Gebäude)" suffix
    connection.execute(
        sa.text(
            """
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Neubau (Gebäude)' WHERE id = 1;
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Anbau (Gebäude)' WHERE id = 2;
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Umbau (Gebäude)' WHERE id = 3;
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Sanierung (Gebäude)' WHERE id = 4;
        """
        )
    )
    # Insert new entry "Sonstiges" (id=6); Abriss (id=5) stays unchanged
    connection.execute(
        sa.text(
            """
        INSERT INTO klimarelevanzpruefung_vorhaben (id, name) VALUES (6, 'Sonstiges')
        ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
        """
        )
    )

    # --- klimarelevanzpruefung_energiestandard ---
    # Clear all rows (ON DELETE SET NULL will null FK refs in eingabe tables)
    connection.execute(
        sa.text("DELETE FROM klimarelevanzpruefung_energiestandard;")
    )
    # Re-insert with KfW-Effizienzhaus Denkmal added at id=2, others shifted to 3–9
    connection.execute(
        sa.text(
            """
        INSERT INTO klimarelevanzpruefung_energiestandard (id, name) VALUES
            (1, 'kein Standard'),
            (2, 'KfW-Effizienzhaus Denkmal'),
            (3, 'KfW-Effizienzhaus 115'),
            (4, 'KfW-Effizienzhaus 100'),
            (5, 'KfW-Effizienzhaus 85'),
            (6, 'KfW-Effizienzhaus 70'),
            (7, 'KfW-Effizienzhaus 55'),
            (8, 'KfW-Effizienzhaus 40 (Plus)'),
            (9, 'Passivhaus (PHPP)');
        """
        )
    )

    # --- klimarelevanzpruefung_vorhaben_energiestandard ---
    connection.execute(
        sa.text("DELETE FROM klimarelevanzpruefung_vorhaben_energiestandard;")
    )
    connection.execute(
        sa.text(
            """
        INSERT INTO klimarelevanzpruefung_vorhaben_energiestandard (vorhaben_id, energiestandard_id) VALUES
            -- Neubau (Gebäude) (1) & Anbau (Gebäude) (2): KfW 55, KfW 40 (Plus), Passivhaus
            (1, 7), (1, 8), (1, 9),
            (2, 7), (2, 8), (2, 9),
            -- Umbau (Gebäude) (3) & Sanierung (Gebäude) (4): all options
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
            (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9);
        """
        )
    )


def downgrade() -> None:
    connection = op.get_bind()

    # Restore vorhaben_energiestandard
    connection.execute(
        sa.text("DELETE FROM klimarelevanzpruefung_vorhaben_energiestandard;")
    )
    connection.execute(
        sa.text(
            """
        INSERT INTO klimarelevanzpruefung_vorhaben_energiestandard (vorhaben_id, energiestandard_id) VALUES
            (1, 6), (1, 7), (1, 8),
            (2, 6), (2, 7), (2, 8),
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
            (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8);
        """
        )
    )

    # Restore energiestandard
    connection.execute(
        sa.text("DELETE FROM klimarelevanzpruefung_energiestandard;")
    )
    connection.execute(
        sa.text(
            """
        INSERT INTO klimarelevanzpruefung_energiestandard (id, name) VALUES
            (1, 'kein Standard'),
            (2, 'KfW-Effizienzhaus 115'),
            (3, 'KfW-Effizienzhaus 100'),
            (4, 'KfW-Effizienzhaus 85'),
            (5, 'KfW-Effizienzhaus 70'),
            (6, 'KfW-Effizienzhaus 55'),
            (7, 'KfW-Effizienzhaus 40 (Plus)'),
            (8, 'Passivhaus (PHPP)');
        """
        )
    )

    # Restore vorhaben names
    connection.execute(
        sa.text(
            """
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Neubau' WHERE id = 1;
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Anbau' WHERE id = 2;
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Umbau' WHERE id = 3;
        UPDATE klimarelevanzpruefung_vorhaben SET name = 'Sanierung' WHERE id = 4;
        """
        )
    )
    connection.execute(
        sa.text("DELETE FROM klimarelevanzpruefung_vorhaben WHERE id = 6;")
    )
