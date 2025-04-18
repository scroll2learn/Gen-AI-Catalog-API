"""added_field_in_layout_model

Revision ID: 68eb1f429004
Revises: caa2bf588ead
Create Date: 2025-03-17 14:17:47.711460

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '68eb1f429004'
down_revision = 'caa2bf588ead'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('layout_fields', sa.Column('lyt_fld_source_data_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('layout_fields', 'lyt_fld_source_data_type', schema='catalogdb')
    # ### end Alembic commands ###