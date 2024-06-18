"""m2m table

Revision ID: 78609a0def31
Revises: 90279c3a5f95
Create Date: 2024-05-29 13:36:53.744686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78609a0def31'
down_revision: Union[str, None] = '90279c3a5f95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seed_m2m_seedcollection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seed_id', sa.Integer(), nullable=True),
    sa.Column('seedcollection_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['seed_id'], ['seeds.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['seedcollection_id'], ['seeds_collection.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'seeds', ['id'])
    op.create_unique_constraint(None, 'seeds_collection', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'seeds_collection', type_='unique')
    op.drop_constraint(None, 'seeds', type_='unique')
    op.drop_table('seed_m2m_seedcollection')
    # ### end Alembic commands ###