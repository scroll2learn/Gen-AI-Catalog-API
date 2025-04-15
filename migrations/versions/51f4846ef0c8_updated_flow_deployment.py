"""updated flow deployment

Revision ID: 51f4846ef0c8
Revises: 9f8a899a4d2e
Create Date: 2024-10-29 08:37:31.984829

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON  # Required for JSON type
from app.core.config import Config

# revision identifiers, used by Alembic.
revision = '51f4846ef0c8'
down_revision = '9f8a899a4d2e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Update flow_lock_status to nullable
    op.alter_column(
        "flow_deployment",
        "flow_lock_status",
        existing_type=sa.Boolean,
        nullable=True
    )

def downgrade() -> None:
    # Revert flow_lock_status to non-nullable
    op.alter_column(
        "flow_deployment",
        "flow_lock_status",
        existing_type=sa.Boolean,
        nullable=False
    )
