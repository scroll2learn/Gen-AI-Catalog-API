"""changed_env_field

Revision ID: 5758a2bacf7d
Revises: 7b25fd191bea
Create Date: 2024-08-29 13:19:17.856157

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '5758a2bacf7d'
down_revision = '7b25fd191bea'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'project_environment', 'codes_dtl', ['cloud_provider_cd'], ['id'], source_schema='catalogdb', referent_schema='catalogdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project_environment', schema='catalogdb', type_='foreignkey')
    # ### end Alembic commands ###