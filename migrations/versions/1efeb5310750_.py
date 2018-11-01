"""empty message

Revision ID: 1efeb5310750
Revises: 2867da1f695b
Create Date: 2018-11-01 17:18:47.276000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1efeb5310750'
down_revision = '2867da1f695b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('front_user', 'telephone',
               existing_type=mysql.VARCHAR(length=11),
               type_=sa.String(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('front_user', 'telephone',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=11),
               existing_nullable=False)
    # ### end Alembic commands ###
