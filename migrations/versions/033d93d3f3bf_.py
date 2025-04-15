"""empty message

Revision ID: 033d93d3f3bf
Revises: cc2a6f5946bd, e992778b14c9
Create Date: 2025-02-19 03:50:49.794929

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = '033d93d3f3bf'
down_revision = ('cc2a6f5946bd', 'e992778b14c9')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass