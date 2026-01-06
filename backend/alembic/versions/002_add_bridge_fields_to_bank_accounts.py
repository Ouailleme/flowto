"""Add bridge_user_uuid and balance to bank_accounts

Revision ID: 002
Revises: 001
Create Date: 2026-01-06 02:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to bank_accounts
    op.add_column('bank_accounts', sa.Column('bridge_user_uuid', sa.String(length=255), nullable=True))
    op.add_column('bank_accounts', sa.Column('balance', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'))
    
    # Make bridge_account_id nullable (for manual accounts)
    op.alter_column('bank_accounts', 'bridge_account_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    
    # Make bridge_item_id nullable (for manual accounts)
    op.alter_column('bank_accounts', 'bridge_item_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    
    # Create index on bridge_user_uuid
    op.create_index(op.f('ix_bank_accounts_bridge_user_uuid'), 'bank_accounts', ['bridge_user_uuid'], unique=False)


def downgrade() -> None:
    # Drop index
    op.drop_index(op.f('ix_bank_accounts_bridge_user_uuid'), table_name='bank_accounts')
    
    # Revert nullability
    op.alter_column('bank_accounts', 'bridge_item_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    
    op.alter_column('bank_accounts', 'bridge_account_id',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    
    # Drop columns
    op.drop_column('bank_accounts', 'balance')
    op.drop_column('bank_accounts', 'bridge_user_uuid')

