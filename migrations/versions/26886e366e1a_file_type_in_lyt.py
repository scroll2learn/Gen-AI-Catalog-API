"""file_type_in_lyt

Revision ID: 26886e366e1a
Revises: b338e8a320eb
Create Date: 2024-05-18 07:46:41.285159

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '26886e366e1a'
down_revision = 'b338e8a320eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data_source_layout', sa.Column('data_src_file_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    op.add_column('data_source_layout', sa.Column('data_src_is_history_required', sa.Boolean(), nullable=True), schema='catalogdb')
    op.alter_column('pipeline_sources', 'pipeline_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema='catalogdb')
    op.drop_constraint('pipeline_sources_pipeline_id_fkey', 'pipeline_sources', schema='catalogdb', type_='foreignkey')
    op.create_foreign_key(None, 'pipeline_sources', 'pipelines', ['pipeline_id'], ['pipeline_id'], source_schema='catalogdb', referent_schema='catalogdb', ondelete='CASCADE')
    op.alter_column('pipeline_targets', 'pipeline_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema='catalogdb')
    op.drop_constraint('pipeline_targets_pipeline_id_fkey', 'pipeline_targets', schema='catalogdb', type_='foreignkey')
    op.create_foreign_key(None, 'pipeline_targets', 'pipelines', ['pipeline_id'], ['pipeline_id'], source_schema='catalogdb', referent_schema='catalogdb', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pipeline_targets', schema='catalogdb', type_='foreignkey')
    op.create_foreign_key('pipeline_targets_pipeline_id_fkey', 'pipeline_targets', 'pipelines', ['pipeline_id'], ['pipeline_id'], source_schema='catalogdb', referent_schema='catalogdb')
    op.alter_column('pipeline_targets', 'pipeline_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema='catalogdb')
    op.drop_constraint(None, 'pipeline_sources', schema='catalogdb', type_='foreignkey')
    op.create_foreign_key('pipeline_sources_pipeline_id_fkey', 'pipeline_sources', 'pipelines', ['pipeline_id'], ['pipeline_id'], source_schema='catalogdb', referent_schema='catalogdb')
    op.alter_column('pipeline_sources', 'pipeline_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema='catalogdb')
    op.drop_column('data_source_layout', 'data_src_is_history_required', schema='catalogdb')
    op.drop_column('data_source_layout', 'data_src_file_type', schema='catalogdb')
    # ### end Alembic commands ###