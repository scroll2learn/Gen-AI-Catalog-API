"""secret_name_conn_model

Revision ID: d20537b86b5a
Revises: 931d63dbe67b
Create Date: 2025-03-19 12:31:43.993160

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = 'd20537b86b5a'
down_revision = '931d63dbe67b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bh_connection_config', sa.Column('secret_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bh_connection_config', 'secret_name', schema='catalogdb')
    # ### end Alembic commands ###