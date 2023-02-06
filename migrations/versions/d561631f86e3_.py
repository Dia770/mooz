"""empty message

Revision ID: d561631f86e3
Revises: bc40f2b47a84
Create Date: 2022-12-21 12:59:05.833005

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd561631f86e3'
down_revision = 'bc40f2b47a84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('codes', schema=None) as batch_op:
        batch_op.alter_column('hashcode',
                              existing_type=mysql.VARCHAR(length=128),
                              type_=sa.String(length=256),
                              existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('codes', schema=None) as batch_op:
        batch_op.alter_column('hashcode',
                              existing_type=sa.String(length=256),
                              type_=mysql.VARCHAR(length=128),
                              existing_nullable=False)

    # ### end Alembic commands ###
