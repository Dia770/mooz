"""empty message

Revision ID: a35bff3e00b8
Revises: e33b57ff3ff9
Create Date: 2023-01-31 13:21:06.446435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a35bff3e00b8'
down_revision = 'e33b57ff3ff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('station_id', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('error', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stations', schema=None) as batch_op:
        batch_op.drop_column('error')
        batch_op.drop_column('station_id')

    # ### end Alembic commands ###
