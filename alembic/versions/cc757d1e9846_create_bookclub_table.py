"""Create BookClub table

Revision ID: cc757d1e9846
Revises: ded1feefaafe
Create Date: 2021-03-13 19:41:58.664310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc757d1e9846'
down_revision = 'ded1feefaafe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'book_club',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('server_id', sa.Integer(), nullable=False),
        sa.Column('channel_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('interval', sa.Integer(), nullable=True),
        sa.Column('start', sa.Integer(), nullable=True),
        sa.Column('end', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_table('book_club')
