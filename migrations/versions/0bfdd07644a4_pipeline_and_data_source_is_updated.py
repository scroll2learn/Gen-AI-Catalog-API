"""pipeline and data-source is updated

Revision ID: 0bfdd07644a4
Revises: bee8cbc65d91
Create Date: 2025-01-06 11:00:15.016611

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '0bfdd07644a4'
down_revision = 'bee8cbc65d91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data_source', sa.Column('file_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    op.add_column('data_source', sa.Column('connection_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    op.add_column('data_source', sa.Column('file_path_prefix', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    op.add_column('pipeline', sa.Column('pipeline_json', sa.JSON(), nullable=True), schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pipeline', 'pipeline_json', schema='catalogdb')
    op.drop_column('data_source', 'file_path_prefix', schema='catalogdb')
    op.drop_column('data_source', 'connection_type', schema='catalogdb')
    op.drop_column('data_source', 'file_name', schema='catalogdb')
    # ### end Alembic commands ###