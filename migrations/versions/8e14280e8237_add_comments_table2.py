"""add comments table2

Revision ID: 8e14280e8237
Revises: 7838cce94486
Create Date: 2023-10-07 19:55:23.744217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e14280e8237'
down_revision = '7838cce94486'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.String(length=68), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###