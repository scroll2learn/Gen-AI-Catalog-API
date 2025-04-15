"""bh_project_env_changes

Revision ID: 1ce7f11dfa7f
Revises: 0f1054a001f7
Create Date: 2024-08-23 13:27:18.842322

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '1ce7f11dfa7f'
down_revision = '0f1054a001f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_environment', sa.Column('gcp_project_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    op.drop_constraint('project_environment_bh_project_id_fkey', 'project_environment', schema='catalogdb', type_='foreignkey')
    op.drop_column('project_environment', 'bh_project_id', schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_environment', sa.Column('bh_project_id', sa.INTEGER(), autoincrement=False, nullable=True), schema='catalogdb')
    op.create_foreign_key('project_environment_bh_project_id_fkey', 'project_environment', 'bh_project', ['bh_project_id'], ['bh_project_id'], source_schema='catalogdb', referent_schema='catalogdb')
    op.drop_column('project_environment', 'gcp_project_id', schema='catalogdb')
    # ### end Alembic commands ###