"""create secret santa table

Revision ID: ded1feefaafe
Revises: 833d20d78e2a
Create Date: 2020-09-12 00:15:07.068825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ded1feefaafe'
down_revision = '833d20d78e2a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'secret_santa',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('server_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(255), nullable=False),
        sa.Column('note', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_table('secret_santa')

