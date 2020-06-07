"""empty message

Revision ID: 900c17ebefe4
Revises: 715ab2d7605d
Create Date: 2020-06-06 23:32:47.898713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '900c17ebefe4'
down_revision = '715ab2d7605d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('is_favourite', sa.Boolean(), nullable=True))
    op.add_column('images', sa.Column('path', sa.String(), nullable=True))
    op.drop_column('images', 'favourite')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('favourite', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('images', 'path')
    op.drop_column('images', 'is_favourite')
    # ### end Alembic commands ###