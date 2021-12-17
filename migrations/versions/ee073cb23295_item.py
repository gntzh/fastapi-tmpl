"""Item

Revision ID: ee073cb23295
Revises: 4acd0291b040
Create Date: 2021-09-26 19:43:13.146854

"""
import sqlalchemy as sa
from alembic import op

import src

# revision identifiers, used by Alembic.
revision = "ee073cb23295"
down_revision = "4acd0291b040"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "item",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=40), nullable=True),
        sa.Column("description", sa.String(length=200), nullable=True),
        sa.Column("owner_id", src.libs.sa.uuid.UUID(length=16), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_item_description"), "item", ["description"], unique=False)
    op.create_index(op.f("ix_item_id"), "item", ["id"], unique=False)
    op.create_index(op.f("ix_item_title"), "item", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_item_title"), table_name="item")
    op.drop_index(op.f("ix_item_id"), table_name="item")
    op.drop_index(op.f("ix_item_description"), table_name="item")
    op.drop_table("item")
    # ### end Alembic commands ###