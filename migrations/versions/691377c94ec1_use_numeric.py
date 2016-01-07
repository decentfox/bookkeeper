"""use NUMERIC

Revision ID: 691377c94ec1
Revises: 180c678aa92c
Create Date: 2016-01-07 18:56:07.621991

"""

# revision identifiers, used by Alembic.
revision = '691377c94ec1'
down_revision = '180c678aa92c'
branch_labels = None

from alembic import op


def upgrade():
    op.execute('ALTER TABLE bkr_records ALTER amount TYPE NUMERIC(16, 2)')


def downgrade():
    op.execute('ALTER TABLE bkr_records ALTER amount TYPE INTEGER')
