"""bookkeeper initial

Revision ID: 6bdb37c0e131
Revises: None
Create Date: 2016-01-04 21:49:11.196875

"""

# revision identifiers, used by Alembic.
revision = '6bdb37c0e131'
down_revision = None
branch_labels = ('bookkeeper',)

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.create_table(
        'bkr_accounts',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.Unicode(), nullable=True),
        sa.Column('title', sa.Unicode(), nullable=False),
        sa.Column('direction', sa.SmallInteger(), nullable=False),
        sa.Column('parent_id', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['bkr_accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bkr_companies',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Unicode(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bkr_periods',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('month', sa.SmallInteger(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bkr_users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bkr_users_x_companies',
        sa.Column('users_id', sa.BigInteger(), nullable=True),
        sa.Column('companies_id', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['companies_id'], ['bkr_companies.id'], ),
        sa.ForeignKeyConstraint(['users_id'], ['bkr_users.id'], )
    )
    op.create_table(
        'bkr_vouchers',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('index', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('creator_id', sa.BigInteger(), nullable=False),
        sa.Column('company_id', sa.BigInteger(), nullable=False),
        sa.Column('period_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['bkr_companies.id'], ),
        sa.ForeignKeyConstraint(['creator_id'], ['bkr_users.id'], ),
        sa.ForeignKeyConstraint(['period_id'], ['bkr_periods.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bkr_records',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('summary', sa.Unicode(), nullable=True),
        sa.Column('direction', sa.SmallInteger(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('voucher_id', sa.BigInteger(), nullable=False),
        sa.Column('account_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['bkr_accounts.id'], ),
        sa.ForeignKeyConstraint(['voucher_id'], ['bkr_vouchers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('bkr_records')
    op.drop_table('bkr_vouchers')
    op.drop_table('bkr_users_x_companies')
    op.drop_table('bkr_users')
    op.drop_table('bkr_periods')
    op.drop_table('bkr_companies')
    op.drop_table('bkr_accounts')
