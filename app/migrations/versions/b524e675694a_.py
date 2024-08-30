"""empty message

Revision ID: b524e675694a
Revises: 25ba559139f1
Create Date: 2024-08-30 17:05:47.929337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b524e675694a'
down_revision: Union[str, None] = '25ba559139f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
