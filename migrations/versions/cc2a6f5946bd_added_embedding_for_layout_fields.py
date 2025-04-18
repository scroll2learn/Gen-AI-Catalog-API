"""added_embedding_for_layout_fields

Revision ID: cc2a6f5946bd
Revises: d68577396724
Create Date: 2025-02-14 12:19:48.188036

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW
import pgvector

# revision identifiers, used by Alembic.
revision = 'cc2a6f5946bd'
down_revision = 'd68577396724'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data_source', sa.Column('data_src_embeddings', pgvector.sqlalchemy.vector.VECTOR(dim=1536), nullable=True), schema='catalogdb')
    op.drop_column('data_source', 'data_src_embedding', schema='catalogdb')
    op.add_column('layout_fields', sa.Column('lyt_fld_embedding', pgvector.sqlalchemy.vector.VECTOR(dim=1536), nullable=True), schema='catalogdb')
    op.add_column('layout_fields', sa.Column('lyt_fld_data_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('layout_fields', 'lyt_fld_data_type', schema='catalogdb')
    op.drop_column('layout_fields', 'lyt_fld_embedding', schema='catalogdb')
    op.add_column('data_source', sa.Column('data_src_embedding', pgvector.sqlalchemy.vector.VECTOR(dim=768), autoincrement=False, nullable=True), schema='catalogdb')
    op.drop_column('data_source', 'data_src_embeddings', schema='catalogdb')
    # ### end Alembic commands ###