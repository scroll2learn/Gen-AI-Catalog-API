"""real data for test case

Revision ID: adc392d3577e
Revises: 545a329cb7bb
Create Date: 2024-12-11 10:08:41.865740

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = 'adc392d3577e'
down_revision = '545a329cb7bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open('migrations/sql/data_field.sql') as sql_file:
        sql_commands = sql_file.read().split(';')

    # Execute each command separately
    for command in sql_commands:
        if command.strip():
            op.execute(command)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###