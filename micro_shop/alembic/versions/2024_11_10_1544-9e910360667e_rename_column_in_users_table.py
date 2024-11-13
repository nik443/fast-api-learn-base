"""rename column in users table

Revision ID: 9e910360667e
Revises: f7ca050be76b
Create Date: 2024-11-10 15:44:24.617442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e910360667e'
down_revision: Union[str, None] = 'f7ca050be76b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
