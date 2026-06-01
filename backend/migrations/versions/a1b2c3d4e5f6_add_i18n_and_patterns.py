"""add i18n columns, ui_messages, block_pattern

Revision ID: a1b2c3d4e5f6
Revises: 7fcec3e238c9
Create Date: 2026-06-01 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '7fcec3e238c9'
branch_labels = None
depends_on = None


def upgrade():
    # Per-model i18n map: {"<locale>": {"<field>": <value>}}. server_default so
    # the NOT NULL add is safe on tables that already have rows.
    for table in ("design_profile", "page", "blog_post"):
        with op.batch_alter_table(table, schema=None) as batch_op:
            batch_op.add_column(
                sa.Column("i18n", sa.JSON(), nullable=False, server_default=sa.text("'{}'"))
            )

    op.create_table(
        "ui_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False),
        sa.Column("messages", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("ui_messages", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_ui_messages_locale"), ["locale"], unique=True)

    op.create_table(
        "block_pattern",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("spec", sa.JSON(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("block_pattern", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_block_pattern_slug"), ["slug"], unique=True)


def downgrade():
    with op.batch_alter_table("block_pattern", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_block_pattern_slug"))
    op.drop_table("block_pattern")

    with op.batch_alter_table("ui_messages", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_ui_messages_locale"))
    op.drop_table("ui_messages")

    for table in ("blog_post", "page", "design_profile"):
        with op.batch_alter_table(table, schema=None) as batch_op:
            batch_op.drop_column("i18n")
