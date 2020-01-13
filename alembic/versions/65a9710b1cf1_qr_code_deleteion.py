"""qr code deleteion

Revision ID: 65a9710b1cf1
Revises: 833d20d78e2a
Create Date: 2020-01-12 22:18:06.906395

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '65a9710b1cf1'
down_revision = '833d20d78e2a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'qr_code_auto_deletion',
        sa.Column('server_id', sa.Integer, primary_key=True),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('logging_channel_id', sa.Integer()),
    )


def downgrade():
    op.drop_table('qr_code_auto_deletion')
