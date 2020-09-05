"""create secret santa table

Revision ID: 19bb89491da6
Revises: dab38e6e2f26
Create Date: 2020-09-04 20:03:53.021774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19bb89491da6'
down_revision = 'dab38e6e2f26'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'secret_santa',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('server_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('note', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_table('secret_santa')
