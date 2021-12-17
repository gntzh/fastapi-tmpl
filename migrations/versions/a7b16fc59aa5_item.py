"""Item

Revision ID: a7b16fc59aa5
Revises: ee073cb23295
Create Date: 2021-09-26 19:44:37.406453

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "a7b16fc59aa5"
down_revision = "ee073cb23295"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_item_description", table_name="item")
    op.drop_index("ix_item_id", table_name="item")
    op.drop_index("ix_item_title", table_name="item")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_item_title", "item", ["title"], unique=False)
    op.create_index("ix_item_id", "item", ["id"], unique=False)
    op.create_index("ix_item_description", "item", ["description"], unique=False)
    # ### end Alembic commands ###