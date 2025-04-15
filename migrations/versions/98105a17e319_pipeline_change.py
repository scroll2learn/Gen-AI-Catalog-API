"""pipeline_change

Revision ID: 98105a17e319
Revises: 26886e366e1a
Create Date: 2024-05-26 12:04:10.325018

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '98105a17e319'
down_revision = '26886e366e1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pipelines', sa.Column('data_src_id', sa.Integer(), nullable=True), schema='catalogdb')
    op.create_foreign_key(None, 'pipelines', 'data_source', ['data_src_id'], ['data_src_id'], source_schema='catalogdb', referent_schema='catalogdb')
    op.execute("UPDATE pipelines SET data_src_id = 1 WHERE pipeline_id=1")
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pipelines', schema='catalogdb', type_='foreignkey')
    op.drop_column('pipelines', 'data_src_id', schema='catalogdb')
    # ### end Alembic commands ###