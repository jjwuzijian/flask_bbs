"""empty message

Revision ID: 358fcce11aa2
Revises: 2e5d9732a399
Create Date: 2018-10-12 23:10:01.975000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '358fcce11aa2'
down_revision = '2e5d9732a399'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banner', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('banner', 'create_time')
    # ### end Alembic commands ###