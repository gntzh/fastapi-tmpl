"""rename

Revision ID: f222e6d3bcf6
Revises: d518cf4bffee
Create Date: 2021-09-26 18:58:34.251732

"""
import sqlalchemy as sa
from alembic import op

import src

# revision identifiers, used by Alembic.
revision = "f222e6d3bcf6"
down_revision = "d518cf4bffee"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("date_joined", src.libs.sa.timezone.TZDateTime(), nullable=True),
    )
    op.drop_column("user", "join_date")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("join_date", sa.DATETIME(), nullable=True))
    op.drop_column("user", "date_joined")
    # ### end Alembic commands ###
