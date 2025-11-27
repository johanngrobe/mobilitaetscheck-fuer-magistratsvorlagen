"""rename sequences

Revision ID: bcd26d6bce92
Revises: b183a5107041
Create Date: 2025-09-15 13:21:36.776681

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bcd26d6bce92"
down_revision: Union[str, None] = "b183a5107041"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # climate_submission_id_seq -> klimacheck_eingabe_id_seq
    op.execute(
        "ALTER SEQUENCE climate_submission_id_seq RENAME TO klimacheck_eingabe_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE klimacheck_eingabe_id_seq OWNED BY klimacheck_eingabe.id"
    )
    op.execute(
        "ALTER TABLE klimacheck_eingabe ALTER COLUMN id SET DEFAULT nextval('klimacheck_eingabe_id_seq')"
    )

    # indicator_id_seq -> indikator_id_seq
    op.execute("ALTER SEQUENCE indicator_id_seq RENAME TO indikator_id_seq")
    op.execute("ALTER SEQUENCE indikator_id_seq OWNED BY indikator.id")
    op.execute(
        "ALTER TABLE indikator ALTER COLUMN id SET DEFAULT nextval('indikator_id_seq')"
    )

    # mobility_result_id_seq -> mobilitaetscheck_eingabe_ziel_ober_id_seq
    op.execute(
        "ALTER SEQUENCE mobility_result_id_seq RENAME TO mobilitaetscheck_eingabe_ziel_ober_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_eingabe_ziel_ober_id_seq OWNED BY mobilitaetscheck_eingabe_ziel_ober.id"
    )
    op.execute(
        "ALTER TABLE mobilitaetscheck_eingabe_ziel_ober ALTER COLUMN id SET DEFAULT nextval('mobilitaetscheck_eingabe_ziel_ober_id_seq')"
    )

    # mobility_result_sub_id_seq -> mobilitaetscheck_eingabe_ziel_unter_id_seq
    op.execute(
        "ALTER SEQUENCE mobility_result_sub_id_seq RENAME TO mobilitaetscheck_eingabe_ziel_unter_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_eingabe_ziel_unter_id_seq OWNED BY mobilitaetscheck_eingabe_ziel_unter.id"
    )
    op.execute(
        "ALTER TABLE mobilitaetscheck_eingabe_ziel_unter ALTER COLUMN id SET DEFAULT nextval('mobilitaetscheck_eingabe_ziel_unter_id_seq')"
    )

    # mobility_submission_id_seq -> mobilitaetscheck_eingabe_id_seq
    op.execute(
        "ALTER SEQUENCE mobility_submission_id_seq RENAME TO mobilitaetscheck_eingabe_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_eingabe_id_seq OWNED BY mobilitaetscheck_eingabe.id"
    )
    op.execute(
        "ALTER TABLE mobilitaetscheck_eingabe ALTER COLUMN id SET DEFAULT nextval('mobilitaetscheck_eingabe_id_seq')"
    )

    # municipality_id_seq -> gemeinde_id_seq
    op.execute("ALTER SEQUENCE municipality_id_seq RENAME TO gemeinde_id_seq")
    op.execute("ALTER SEQUENCE gemeinde_id_seq OWNED BY gemeinde.id")
    op.execute(
        "ALTER TABLE gemeinde ALTER COLUMN id SET DEFAULT nextval('gemeinde_id_seq')"
    )

    # key_target_id_seq -> mobilitaetscheck_ziel_ober_id_seq
    op.execute(
        "ALTER SEQUENCE key_target_id_seq RENAME TO mobilitaetscheck_ziel_ober_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_ziel_ober_id_seq OWNED BY mobilitaetscheck_ziel_ober.id"
    )
    op.execute(
        "ALTER TABLE mobilitaetscheck_ziel_ober ALTER COLUMN id SET DEFAULT nextval('mobilitaetscheck_ziel_ober_id_seq')"
    )

    # sub_target_id_seq -> mobilitaetscheck_ziel_unter_id_seq
    op.execute(
        "ALTER SEQUENCE sub_target_id_seq RENAME TO mobilitaetscheck_ziel_unter_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_ziel_unter_id_seq OWNED BY mobilitaetscheck_ziel_unter.id"
    )
    op.execute(
        "ALTER TABLE mobilitaetscheck_ziel_unter ALTER COLUMN id SET DEFAULT nextval('mobilitaetscheck_ziel_unter_id_seq')"
    )

    # text_block_id_seq -> textblock_id_seq
    op.execute("ALTER SEQUENCE text_block_id_seq RENAME TO textblock_id_seq")
    op.execute("ALTER SEQUENCE textblock_id_seq OWNED BY textblock.id")
    op.execute(
        "ALTER TABLE textblock ALTER COLUMN id SET DEFAULT nextval('textblock_id_seq')"
    )

    op.execute(
        """
    DO $$
    DECLARE
        rec RECORD;
    BEGIN
        FOR rec IN
            SELECT
                c.oid::regclass::text AS table_name,
                a.attname AS column_name,
                seq.relname AS sequence_name
            FROM pg_class c
            JOIN pg_attribute a
              ON a.attrelid = c.oid
            JOIN pg_attrdef d
              ON d.adrelid = c.oid AND d.adnum = a.attnum
            JOIN pg_class seq
              ON seq.relkind = 'S'
             AND pg_get_expr(d.adbin, d.adrelid) LIKE 'nextval(%' || seq.relname || '%::regclass)'
            WHERE c.relkind = 'r'
              AND a.attnum > 0
              AND NOT a.attisdropped
        LOOP
            EXECUTE format(
                'SELECT setval(''%s'', COALESCE((SELECT MAX(%I) FROM %s), 1), true);',
                rec.sequence_name, rec.column_name, rec.table_name
            );
        END LOOP;
    END$$;
    """
    )


def downgrade() -> None:
    # Reverse renames
    op.execute(
        "ALTER SEQUENCE klimacheck_eingabe_id_seq RENAME TO climate_submission_id_seq"
    )
    op.execute("ALTER SEQUENCE indikator_id_seq RENAME TO indicator_id_seq")
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_eingabe_ziel_ober_id_seq RENAME TO mobility_result_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_eingabe_ziel_unter_id_seq RENAME TO mobility_result_sub_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_eingabe_id_seq RENAME TO mobility_submission_id_seq"
    )
    op.execute("ALTER SEQUENCE gemeinde_id_seq RENAME TO municipality_id_seq")
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_ziel_ober_id_seq RENAME TO key_target_id_seq"
    )
    op.execute(
        "ALTER SEQUENCE mobilitaetscheck_ziel_unter_id_seq RENAME TO sub_target_id_seq"
    )
    op.execute("ALTER SEQUENCE textblock_id_seq RENAME TO text_block_id_seq")
