"""merge heads

Revision ID: d760fdcfad2b
Revises: add_address_fields_to_location, fb1c786f8224
Create Date: 2025-03-23 11:12:08.274359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd760fdcfad2b'
down_revision: Union[str, None] = ('add_address_fields_to_location', 'fb1c786f8224')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
