"""add revision (surface snapshots for undo/restore)

Revision ID: d1e2f3a4b5c6
Revises: c1d2e3f4a5b6
Create Date: 2026-06-02 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1e2f3a4b5c6'
down_revision = 'c1d2e3f4a5b6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "revision",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("surface", sa.String(length=128), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("kind", sa.String(length=16), nullable=False, server_default="sections"),
        sa.Column("label", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("snapshot", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("revision", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_revision_surface"), ["surface"], unique=False)
        batch_op.create_index("ix_revision_surface_locale", ["surface", "locale"], unique=False)


def downgrade():
    with op.batch_alter_table("revision", schema=None) as batch_op:
        batch_op.drop_index("ix_revision_surface_locale")
        batch_op.drop_index(batch_op.f("ix_revision_surface"))
    op.drop_table("revision")
