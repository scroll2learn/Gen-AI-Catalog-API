"""add_unique_constraint_to_pipeline_parameters

Revision ID: 0d0a9fae4db9
Revises: 53fc63f9dd24
Create Date: 2025-02-20 04:06:38.717281

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '0d0a9fae4db9'
down_revision = '53fc63f9dd24'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_pipeline_parameter', 'pipeline_parameter', ['pipeline_id', 'parameter_name', 'parameter_type'], schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_pipeline_parameter', 'pipeline_parameter', schema='catalogdb', type_='unique')
    # ### end Alembic commands ###