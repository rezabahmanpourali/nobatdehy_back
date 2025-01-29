from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '405cdec8cff7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.drop_index('ix_comments_id', table_name='comments')
    op.drop_table('comments')
    op.drop_index('ix_imageModel_id', table_name='imageModel')
    op.drop_table('imageModel')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_category_id', table_name='category')
    
    op.drop_constraint('barber_hair_model_category_id_fkey', 'barber_hair_model', type_='foreignkey')
    op.drop_constraint('images_category_id_fkey', 'images', type_='foreignkey')
    op.drop_table('category')
    
    op.drop_constraint('barber_hair_model_hair_model_id_fkey', 'barber_hair_model', type_='foreignkey')
    op.drop_constraint('images_hair_model_id_fkey', 'images', type_='foreignkey')
    op.drop_table('hair_model')
    
    op.drop_index('ix_barber_hair_model_id', table_name='barber_hair_model')
    op.drop_table('barber_hair_model')
    op.drop_index('ix_images_id', table_name='images')
    op.drop_table('images')
    op.drop_index('ix_location_id', table_name='location')
    op.drop_table('location')
    op.add_column('barber', sa.Column('name', sa.String(), nullable=True))
    op.create_index(op.f('ix_barber_name'), 'barber', ['name'], unique=False)
    op.drop_constraint('barber_barber_shop_id_fkey', 'barber', type_='foreignkey')
    op.drop_column('barber', 'barber_name')
    op.drop_column('barber', 'barber_shop_id')
    op.add_column('barber_shop', sa.Column('name', sa.String(), nullable=True))
    op.create_index(op.f('ix_barber_shop_name'), 'barber_shop', ['name'], unique=False)
    op.drop_column('barber_shop', 'is_active')
    op.drop_column('barber_shop', 'address')
    op.drop_column('barber_shop', 'barber_shop_name')
    op.drop_column('barber_shop', 'location_id')
    op.drop_column('barber_shop', 'barbers_detail')
    op.drop_column('barber_shop', 'shop_type')

def downgrade() -> None:
    op.add_column('barber_shop', sa.Column('shop_type', postgresql.ENUM(
        'SEEN_RECENTLY', 'TOP_BARBERS', 'HOTTEST_BARBERS', name='barbershoptype'), autoincrement=False, nullable=True))
    op.add_column('barber_shop', sa.Column('barbers_detail', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('barber_shop', sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('barber_shop', sa.Column('barber_shop_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('barber_shop', sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('barber_shop', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_barber_shop_name'), table_name='barber_shop')
    op.drop_column('barber_shop', 'name')
    op.add_column('barber', sa.Column('barber_shop_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('barber', sa.Column('barber_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('barber_barber_shop_id_fkey', 'barber', 'barber_shop', ['barber_shop_id'], ['id'])
    op.drop_index(op.f('ix_barber_name'), table_name='barber')
    op.drop_column('barber', 'name')
