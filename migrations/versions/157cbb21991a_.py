"""empty message

Revision ID: 157cbb21991a
Revises: 4de0b91f6245
Create Date: 2023-02-02 00:30:03.340567

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '157cbb21991a'
down_revision = '4de0b91f6245'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('connexions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_user', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('username', sa.String(length=64), nullable=True))
        batch_op.drop_column('consumed_by')
        batch_op.drop_column('success')
        batch_op.drop_column('generated_by')
        batch_op.drop_column('code_used')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('connexions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code_used', mysql.VARCHAR(length=64), nullable=True))
        batch_op.add_column(sa.Column('generated_by', mysql.VARCHAR(length=64), nullable=True))
        batch_op.add_column(sa.Column('success', mysql.VARCHAR(length=10), nullable=True))
        batch_op.add_column(sa.Column('consumed_by', mysql.VARCHAR(length=64), nullable=True))
        batch_op.drop_column('username')
        batch_op.drop_column('id_user')

    # ### end Alembic commands ###
