"""Add address fields to location table

Revision ID: add_address_fields_to_location
Revises: fb1c786f8224
Create Date: 2024-03-22 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_address_fields_to_location'
down_revision = 'fb1c786f8224'
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