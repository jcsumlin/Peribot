"""Deop Secret Santa table

Revision ID: 4077902180f3
Revises: 9b2cebb5142f
Create Date: 2021-03-13 23:14:19.739043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4077902180f3'
down_revision = '9b2cebb5142f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('secret_santa')
    op.drop_table('qr_code_auto_deletion')


def downgrade():
    pass
