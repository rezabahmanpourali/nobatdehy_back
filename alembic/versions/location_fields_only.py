"""Add location fields only

Revision ID: location_fields_only
Revises: bb89d4b67f59
Create Date: 2024-03-22 09:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'location_fields_only'
down_revision = 'bb89d4b67f59'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add new columns to location table
    op.add_column('location', sa.Column('address', sa.String(), nullable=True))
    op.add_column('location', sa.Column('city', sa.String(), nullable=True))
    op.add_column('location', sa.Column('state', sa.String(), nullable=True))
    op.add_column('location', sa.Column('postal_code', sa.String(), nullable=True))
    op.add_column('location', sa.Column('country', sa.String(), nullable=True))

def downgrade() -> None:
    # Remove the added columns
    op.drop_column('location', 'country')
    op.drop_column('location', 'postal_code')
    op.drop_column('location', 'state')
    op.drop_column('location', 'city')
    op.drop_column('location', 'address') 