"""data_setup

Revision ID: 5d60c257fcde
Revises: e0bd6518e86b
Create Date: 2024-04-22 04:42:33.573878

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '5d60c257fcde'
down_revision = 'e0bd6518e86b'
branch_labels = None
depends_on = None


def upgrade():
    # 1: Read SQL commands from the file "CMDB Inserts"
    with open('migrations/sql/cd_tbl_insert.sql') as sql_file:
        sql_commands = sql_file.read().split(';')

    # Execute each command separately
    for command in sql_commands:
        if command.strip():
            op.execute(command)

    # 2: Read SQL commands from the file "Field Validation rules"
    with open('migrations/sql/fld_dq_template.sql') as sql_file:
        sql_commands = sql_file.read().split(';')

    # Execute each command separately
    for command in sql_commands:
        if command.strip():
            op.execute(command)

    # 3: Read SQL commands from the file "Demo Project Setup"
    with open('migrations/sql/demo_project_setup.sql') as sql_file:
        sql_commands = sql_file.read().split(';')

    # Execute each command separately
    for command in sql_commands:
        if command.strip():
            op.execute(command)

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
