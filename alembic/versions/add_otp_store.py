"""Add OTP store table

Revision ID: add_otp_store
Revises: bb89d4b67f59
Create Date: 2024-03-22 08:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision = 'add_otp_store'
down_revision = 'bb89d4b67f59'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create otp_store table
    op.create_table(
        'otp_store',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('otp', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_otp_store_id'), 'otp_store', ['id'], unique=False)
    op.create_index(op.f('ix_otp_store_phone'), 'otp_store', ['phone'], unique=True)

def downgrade() -> None:
    # Drop otp_store table
    op.drop_index(op.f('ix_otp_store_phone'), table_name='otp_store')
    op.drop_index(op.f('ix_otp_store_id'), table_name='otp_store')
    op.drop_table('otp_store') 