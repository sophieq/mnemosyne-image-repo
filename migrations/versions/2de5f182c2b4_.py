"""empty message

Revision ID: 2de5f182c2b4
Revises: 7c4bf19e5334
Create Date: 2020-06-09 22:38:31.804670

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2de5f182c2b4'
down_revision = '7c4bf19e5334'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('month_uploaded', sa.DateTime(), nullable=True))
    op.drop_column('images', 'date_uploaded')
    op.drop_column('images', 'is_favourite')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('is_favourite', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('images', sa.Column('date_uploaded', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('images', 'month_uploaded')
    # ### end Alembic commands ###
