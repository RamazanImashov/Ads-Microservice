"""ads

Revision ID: e197f1cd0b8e
Revises: d2e139ca0381
Create Date: 2024-10-29 14:12:06.191410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e197f1cd0b8e'
down_revision: Union[str, None] = 'd2e139ca0381'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "advertisements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_advertisements"))
    )


def downgrade() -> None:
    op.drop_table("advertisements")
