"""add comments table2.1

Revision ID: fad2ee383953
Revises: 8e14280e8237
Create Date: 2023-10-07 20:00:34.257700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fad2ee383953'
down_revision = '8e14280e8237'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('user_name',
               existing_type=sa.VARCHAR(length=68),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('user_name',
               existing_type=sa.VARCHAR(length=68),
               nullable=False)

    # ### end Alembic commands ###
