"""Add working hours table

Revision ID: bb89d4b67f59
Revises: 
Create Date: 2024-03-14

"""
from alembic import op
import sqlalchemy as sa
from src.barber_shop.models import DayOfWeek

# revision identifiers, used by Alembic.
revision = 'bb89d4b67f59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create working_hours table with existing enum
    op.create_table(
        'working_hours',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('barber_shop_id', sa.Integer(), nullable=False),
        sa.Column('day_of_week', sa.Enum(DayOfWeek, name='dayofweek', create_type=False), nullable=False),
        sa.Column('opening_time', sa.Time(), nullable=False),
        sa.Column('closing_time', sa.Time(), nullable=False),
        sa.Column('is_closed', sa.Boolean(), server_default='false', nullable=False),
        sa.ForeignKeyConstraint(['barber_shop_id'], ['barber_shop.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_working_hours_id'), 'working_hours', ['id'], unique=False)


def downgrade() -> None:
    # Drop working_hours table
    op.drop_index(op.f('ix_working_hours_id'), table_name='working_hours')
    op.drop_table('working_hours')
