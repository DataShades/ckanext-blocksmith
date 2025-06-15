"""Create blocksmith_snippet table

Revision ID: 998a61a968f8
Revises: 4dda752c7953
Create Date: 2025-06-11 20:15:38.231531

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "998a61a968f8"
down_revision = "4dda752c7953"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "blocksmith_snippet",
        sa.Column("id", sa.Text, primary_key=True, unique=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("html", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "modified_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("readonly", sa.Boolean(), default=False, nullable=False),
        sa.Column("extras", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )

    op.execute(
        """
        INSERT INTO blocksmith_snippet (id, title, name, html, readonly, extras)
        SELECT '1', 'Test Snippet', 'test_snippet', '<p>Test Snippet</p>', TRUE, '{}'
        WHERE NOT EXISTS (
            SELECT 1 FROM blocksmith_snippet WHERE name = 'test_snippet'
        )
        """
    )


def downgrade():
    op.drop_table("blocksmith_snippet")
