"""pipeline_model_changes

Revision ID: dd652955da22
Revises: fc88232d03be
Create Date: 2024-09-13 11:10:37.596090

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dd652955da22'
down_revision = 'fc88232d03be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app_user', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('app_user', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_connection_config', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_connection_config', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_connection_registry', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_connection_registry', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_project', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_project', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_user', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('bh_user', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('connection_dtl', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('connection_dtl', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('customer', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('customer', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('data_source', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('data_source', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('data_source_layout', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('data_source_layout', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('data_source_metadata', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('data_source_metadata', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('fld_dq_types', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('fld_dq_types', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('fld_properties', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('fld_properties', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('fld_recommendations', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('fld_recommendations', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('function_registry', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('function_registry', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('join_on', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('join_on', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('joins', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('joins', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('lake_zone', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('lake_zone', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('layout_fields', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('layout_fields', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('layout_fields_dq', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('layout_fields_dq', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('pipeline_sources', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('pipeline_sources', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.drop_constraint('pipeline_sources_pipeline_id_fkey', 'pipeline_sources', schema='catalogdb', type_='foreignkey')
    op.drop_column('pipeline_sources', 'pipeline_id', schema='catalogdb')
    op.add_column('pipeline_targets', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('pipeline_targets', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.drop_constraint('pipeline_targets_pipeline_id_fkey', 'pipeline_targets', schema='catalogdb', type_='foreignkey')
    op.drop_column('pipeline_targets', 'pipeline_id', schema='catalogdb')
    op.add_column('pipelines', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('pipelines', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('pipelines', sa.Column('bh_project_id', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('pipelines', sa.Column('git_branch', sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema='catalogdb')
    op.drop_constraint('pipelines_data_src_id_fkey', 'pipelines', schema='catalogdb', type_='foreignkey')
    op.drop_column('pipelines', 'pipeline_key', schema='catalogdb')
    op.drop_column('pipelines', 'pipeline_desc', schema='catalogdb')
    op.drop_column('pipelines', 'data_src_id', schema='catalogdb')
    op.drop_column('pipelines', 'pipeline_type_cd', schema='catalogdb')
    op.drop_column('pipelines', 'pipeline_zone_type_cd', schema='catalogdb')
    op.drop_column('pipelines', 'pipeline_schedule', schema='catalogdb')
    op.add_column('project_environment', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('project_environment', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('publish_query_details', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('publish_query_details', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('transform_in_flds', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('transform_in_flds', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('transform_logic', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('transform_logic', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('transform_out_flds', sa.Column('created_by', sa.Integer(), nullable=True), schema='catalogdb')
    op.add_column('transform_out_flds', sa.Column('updated_by', sa.Integer(), nullable=True), schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transform_out_flds', 'updated_by', schema='catalogdb')
    op.drop_column('transform_out_flds', 'created_by', schema='catalogdb')
    op.drop_column('transform_logic', 'updated_by', schema='catalogdb')
    op.drop_column('transform_logic', 'created_by', schema='catalogdb')
    op.drop_column('transform_in_flds', 'updated_by', schema='catalogdb')
    op.drop_column('transform_in_flds', 'created_by', schema='catalogdb')
    op.drop_column('publish_query_details', 'updated_by', schema='catalogdb')
    op.drop_column('publish_query_details', 'created_by', schema='catalogdb')
    op.drop_column('project_environment', 'updated_by', schema='catalogdb')
    op.drop_column('project_environment', 'created_by', schema='catalogdb')
    op.add_column('pipelines', sa.Column('pipeline_schedule', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True), schema='catalogdb')
    op.add_column('pipelines', sa.Column('pipeline_zone_type_cd', sa.INTEGER(), autoincrement=False, nullable=False), schema='catalogdb')
    op.add_column('pipelines', sa.Column('pipeline_type_cd', sa.INTEGER(), autoincrement=False, nullable=False), schema='catalogdb')
    op.add_column('pipelines', sa.Column('data_src_id', sa.INTEGER(), autoincrement=False, nullable=True), schema='catalogdb')
    op.add_column('pipelines', sa.Column('pipeline_desc', sa.VARCHAR(), autoincrement=False, nullable=True), schema='catalogdb')
    op.add_column('pipelines', sa.Column('pipeline_key', sa.VARCHAR(), autoincrement=False, nullable=True), schema='catalogdb')
    op.create_foreign_key('pipelines_data_src_id_fkey', 'pipelines', 'data_source', ['data_src_id'], ['data_src_id'], source_schema='catalogdb', referent_schema='catalogdb')
    op.drop_column('pipelines', 'git_branch', schema='catalogdb')
    op.drop_column('pipelines', 'bh_project_id', schema='catalogdb')
    op.drop_column('pipelines', 'updated_by', schema='catalogdb')
    op.drop_column('pipelines', 'created_by', schema='catalogdb')
    op.add_column('pipeline_targets', sa.Column('pipeline_id', sa.INTEGER(), autoincrement=False, nullable=True), schema='catalogdb')
    op.create_foreign_key('pipeline_targets_pipeline_id_fkey', 'pipeline_targets', 'pipelines', ['pipeline_id'], ['pipeline_id'], source_schema='catalogdb', referent_schema='catalogdb', ondelete='CASCADE')
    op.drop_column('pipeline_targets', 'updated_by', schema='catalogdb')
    op.drop_column('pipeline_targets', 'created_by', schema='catalogdb')
    op.add_column('pipeline_sources', sa.Column('pipeline_id', sa.INTEGER(), autoincrement=False, nullable=True), schema='catalogdb')
    op.create_foreign_key('pipeline_sources_pipeline_id_fkey', 'pipeline_sources', 'pipelines', ['pipeline_id'], ['pipeline_id'], source_schema='catalogdb', referent_schema='catalogdb', ondelete='CASCADE')
    op.drop_column('pipeline_sources', 'updated_by', schema='catalogdb')
    op.drop_column('pipeline_sources', 'created_by', schema='catalogdb')
    op.drop_column('layout_fields_dq', 'updated_by', schema='catalogdb')
    op.drop_column('layout_fields_dq', 'created_by', schema='catalogdb')
    op.drop_column('layout_fields', 'updated_by', schema='catalogdb')
    op.drop_column('layout_fields', 'created_by', schema='catalogdb')
    op.drop_column('lake_zone', 'updated_by', schema='catalogdb')
    op.drop_column('lake_zone', 'created_by', schema='catalogdb')
    op.drop_column('joins', 'updated_by', schema='catalogdb')
    op.drop_column('joins', 'created_by', schema='catalogdb')
    op.drop_column('join_on', 'updated_by', schema='catalogdb')
    op.drop_column('join_on', 'created_by', schema='catalogdb')
    op.drop_column('function_registry', 'updated_by', schema='catalogdb')
    op.drop_column('function_registry', 'created_by', schema='catalogdb')
    op.drop_column('fld_recommendations', 'updated_by', schema='catalogdb')
    op.drop_column('fld_recommendations', 'created_by', schema='catalogdb')
    op.drop_column('fld_properties', 'updated_by', schema='catalogdb')
    op.drop_column('fld_properties', 'created_by', schema='catalogdb')
    op.drop_column('fld_dq_types', 'updated_by', schema='catalogdb')
    op.drop_column('fld_dq_types', 'created_by', schema='catalogdb')
    op.drop_column('data_source_metadata', 'updated_by', schema='catalogdb')
    op.drop_column('data_source_metadata', 'created_by', schema='catalogdb')
    op.drop_column('data_source_layout', 'updated_by', schema='catalogdb')
    op.drop_column('data_source_layout', 'created_by', schema='catalogdb')
    op.drop_column('data_source', 'updated_by', schema='catalogdb')
    op.drop_column('data_source', 'created_by', schema='catalogdb')
    op.drop_column('customer', 'updated_by', schema='catalogdb')
    op.drop_column('customer', 'created_by', schema='catalogdb')
    op.drop_column('connection_dtl', 'updated_by', schema='catalogdb')
    op.drop_column('connection_dtl', 'created_by', schema='catalogdb')
    op.drop_column('bh_user', 'updated_by', schema='catalogdb')
    op.drop_column('bh_user', 'created_by', schema='catalogdb')
    op.drop_column('bh_project', 'updated_by', schema='catalogdb')
    op.drop_column('bh_project', 'created_by', schema='catalogdb')
    op.drop_column('bh_connection_registry', 'updated_by', schema='catalogdb')
    op.drop_column('bh_connection_registry', 'created_by', schema='catalogdb')
    op.drop_column('bh_connection_config', 'updated_by', schema='catalogdb')
    op.drop_column('bh_connection_config', 'created_by', schema='catalogdb')
    op.drop_column('app_user', 'updated_by', schema='catalogdb')
    op.drop_column('app_user', 'created_by', schema='catalogdb')
    # ### end Alembic commands ###