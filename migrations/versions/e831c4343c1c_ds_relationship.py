"""ds_relationship

Revision ID: e831c4343c1c
Revises: 024f3c887558
Create Date: 2025-03-26 09:15:57.964257

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW
import pgvector

# revision identifiers, used by Alembic.
revision = 'e831c4343c1c'
down_revision = '024f3c887558'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data_source', sa.Column('data_src_relationships_embeddings', pgvector.sqlalchemy.vector.VECTOR(dim=768), nullable=True), schema='catalogdb')
    op.add_column('data_source', sa.Column('data_src_relationships', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data_source', 'data_src_relationships', schema='catalogdb')
    op.drop_column('data_source', 'data_src_relationships_embeddings', schema='catalogdb')
    # ### end Alembic commands ###