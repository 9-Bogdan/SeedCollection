"""Init

Revision ID: 90279c3a5f95
Revises: 
Create Date: 2024-05-28 16:23:55.498284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90279c3a5f95'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('confirmed_email', sa.Boolean(), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('seeds_collection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collection_name', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('seeds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('brand_name', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('up_to_date', sa.DateTime(), nullable=True),
    sa.Column('count', sa.Float(), nullable=True),
    sa.Column('count_type', sa.Enum('gramms', 'pack', 'quantity', name='Count_type'), nullable=False),
    sa.Column('category', sa.Enum('vegetable', 'herb', 'flower', 'other', name='category'), nullable=False),
    sa.Column('life_cycle', sa.Enum('annual', 'biennial', 'perennial', 'other', name='life_cycle'), nullable=False),
    sa.Column('culture', sa.Enum('hybrid', 'sort', 'other', name='culture'), nullable=False),
    sa.Column('vegetation_period', sa.Enum('early', 'mid_early', 'average', 'late', 'other', name='vegetation_period'), nullable=False),
    sa.Column('height', sa.Enum('short', 'medium', 'tall', 'other', name='height'), nullable=False),
    sa.Column('flowering_period_start', sa.DateTime(), nullable=True),
    sa.Column('flowering_period_end', sa.DateTime(), nullable=True),
    sa.Column('sow_period_start', sa.DateTime(), nullable=True),
    sa.Column('sow_period_end', sa.DateTime(), nullable=True),
    sa.Column('depth', sa.Float(), nullable=True),
    sa.Column('width', sa.Float(), nullable=True),
    sa.Column('length', sa.Float(), nullable=True),
    sa.Column('germinate_days', sa.Integer(), nullable=True),
    sa.Column('instructions', sa.String(), nullable=True),
    sa.Column('is_pet_safe', sa.Boolean(), nullable=True),
    sa.Column('is_native', sa.Boolean(), nullable=True),
    sa.Column('soil_type', sa.String(), nullable=True),
    sa.Column('start_growing', sa.Enum('direct', 'transplant', 'not_selected', name='start_growing'), nullable=False),
    sa.Column('landing_place', sa.Enum('house', 'garden', 'universal', 'not_selected', name='landing_place'), nullable=False),
    sa.Column('pollination', sa.Enum('self_pollination', 'hand_pollination', 'allogamy', 'not_selected', name='pollination'), nullable=False),
    sa.Column('use_type', sa.Enum('canning', 'cooking', 'freezing', 'fresh', 'not_selected', name='use_type'), nullable=False),
    sa.Column('sunlight', sa.Enum('partial_shade', 'shade', 'light_side', 'not_selected', name='sunlight'), nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['seeds_collection.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seeds')
    op.drop_table('seeds_collection')
    op.drop_table('users')
    # ### end Alembic commands ###