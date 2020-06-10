"""empty message

Revision ID: e1aea6b8b391
Revises: 47c0c0b5f582
Create Date: 2020-06-10 00:25:59.248070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1aea6b8b391'
down_revision = '47c0c0b5f582'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sharing_token', sa.String(length=1000), nullable=True))
    op.drop_column('users', 'sharing_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sharing_link', sa.VARCHAR(length=1000), autoincrement=False, nullable=True))
    op.drop_column('users', 'sharing_token')
    # ### end Alembic commands ###
