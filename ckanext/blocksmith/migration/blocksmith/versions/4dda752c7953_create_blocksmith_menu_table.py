"""Create blocksmith_menu table

Revision ID: 4dda752c7953
Revises: a682a047d28a
Create Date: 2025-04-30 15:41:19.372285

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4dda752c7953"
down_revision = "a682a047d28a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "blocksmith_menu",
        sa.Column("id", sa.Text, primary_key=True, unique=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "modified_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "blocksmith_menu_item",
        sa.Column("id", sa.Text, primary_key=True, unique=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("order", sa.Integer, nullable=False, default=0),
        sa.Column("parent_id", sa.Text, nullable=True),
        sa.Column(
            "menu_id", sa.Text, sa.ForeignKey("blocksmith_menu.id"), nullable=False
        ),
        sa.Column("classes", sa.String, nullable=True),
    )


def downgrade():
    op.drop_table("blocksmith_menu_item")
    op.drop_table("blocksmith_menu")
