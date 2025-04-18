"""audit_events

Revision ID: 00821abaf61b
Revises: 5d60c257fcde
Create Date: 2024-04-22 04:43:56.158339

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '00821abaf61b'
down_revision = '5d60c257fcde'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
        CREATE TABLE IF NOT EXISTS catalogdb.audit_events (
            audit_id serial NOT NULL,
            event_type text NOT NULL,
            bh_timestamp timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
            object_id integer,
            object_type text,
            user_id integer,
            old_object jsonb,
            new_object jsonb,
            comment text,
            PRIMARY KEY (audit_id, bh_timestamp)
        ) PARTITION BY RANGE (bh_timestamp);
    """)

    for year in range(2024, 2044):
        for month in range(1, 13):
            next_month = month + 1 if month != 12 else 1
            next_year = year if month != 12 else year + 1
            op.execute(f"""
                CREATE TABLE IF NOT EXISTS catalogdb.audit_events_{year}_{month:02d} PARTITION OF audit_events
                FOR VALUES FROM ('{year}-{month:02d}-01') TO ('{next_year}-{next_month:02d}-01');
            """)
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    for year in range(2024, 2044):
        for month in range(1, 13):
            op.execute(f"""
                DROP TABLE IF EXISTS audit_events_{year}_{month:02d};
            """)

    op.execute("""
        DROP TABLE IF EXISTS audit_events;
    """)
    # ### end Alembic commands ###
