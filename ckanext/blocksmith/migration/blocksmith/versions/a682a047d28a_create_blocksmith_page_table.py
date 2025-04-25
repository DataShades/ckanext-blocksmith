"""Create blocksmith_page table

Revision ID: a682a047d28a
Revises:
Create Date: 2025-04-25 10:53:29.972260

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = "a682a047d28a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "blocksmith_page",
        sa.Column("id", sa.Text, primary_key=True, unique=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("html", sa.Text(), nullable=True),
        sa.Column("css", sa.Text(), nullable=True),
        sa.Column("editor_data", JSONB(), nullable=False),
        sa.Column("published", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("order_index", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "modified_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
    )


def downgrade():
    op.drop_table("blocksmith_page")
