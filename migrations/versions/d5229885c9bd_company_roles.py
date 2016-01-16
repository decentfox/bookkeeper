"""company_roles

Revision ID: d5229885c9bd
Revises: ad6d7708b1a0
Create Date: 2016-01-15 14:31:49.497572

"""

# revision identifiers, used by Alembic.
revision = 'd5229885c9bd'
down_revision = 'ad6d7708b1a0'
branch_labels = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.create_table(
        'bkr_company_roles',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('company_id', sa.BigInteger(), nullable=False),
        sa.Column('role_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['bkr_companies.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['bkr_roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['bkr_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('bkr_users_x_roles')
    op.drop_table('bkr_users_x_companies')


def downgrade():
    op.create_table(
        'bkr_users_x_companies',
        sa.Column('users_id', sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column('companies_id', sa.BIGINT(), autoincrement=False,
                  nullable=True),
        sa.ForeignKeyConstraint(['companies_id'], ['bkr_companies.id'],
                                name='bkr_users_x_companies_companies_id_fkey'),
        sa.ForeignKeyConstraint(['users_id'], ['bkr_users.id'],
                                name='bkr_users_x_companies_users_id_fkey')
    )
    op.create_table(
        'bkr_users_x_roles',
        sa.Column('users_id', sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column('roles_id', sa.BIGINT(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['roles_id'], ['bkr_roles.id'],
                                name='bkr_users_x_roles_roles_id_fkey'),
        sa.ForeignKeyConstraint(['users_id'], ['bkr_users.id'],
                                name='bkr_users_x_roles_users_id_fkey')
    )
    op.drop_table('bkr_company_roles')
