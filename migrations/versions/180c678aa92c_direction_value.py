"""direction value

Revision ID: 180c678aa92c
Revises: 21788c276468
Create Date: 2016-01-07 14:10:17.103819

"""

# revision identifiers, used by Alembic.
revision = '180c678aa92c'
down_revision = '21788c276468'
branch_labels = None

from alembic import op


def upgrade():
    op.execute('UPDATE bkr_accounts SET direction = -1 WHERE direction = 0')


def downgrade():
    op.execute('UPDATE bkr_accounts SET direction = 0 WHERE direction = -1')
