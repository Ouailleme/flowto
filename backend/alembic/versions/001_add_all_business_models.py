"""Add all business models

Revision ID: 001
Revises: 
Create Date: 2026-01-05 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('old_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('new_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_type'), 'audit_logs', ['entity_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_id'), 'audit_logs', ['entity_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)

    # Create bank_accounts table
    op.create_table(
        'bank_accounts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bridge_account_id', sa.String(length=255), nullable=False),
        sa.Column('bridge_item_id', sa.String(length=255), nullable=False),
        sa.Column('bank_name', sa.String(length=255), nullable=False),
        sa.Column('account_name', sa.String(length=255), nullable=True),
        sa.Column('account_type', sa.String(length=50), nullable=True),
        sa.Column('iban', sa.String(length=100), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_sync_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('bridge_account_id')
    )
    op.create_index(op.f('ix_bank_accounts_user_id'), 'bank_accounts', ['user_id'], unique=False)
    op.create_index(op.f('ix_bank_accounts_bridge_account_id'), 'bank_accounts', ['bridge_account_id'], unique=True)
    op.create_index(op.f('ix_bank_accounts_bridge_item_id'), 'bank_accounts', ['bridge_item_id'], unique=False)

    # Create invoices table
    op.create_table(
        'invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('client_name', sa.String(length=255), nullable=False),
        sa.Column('client_email', sa.String(length=255), nullable=True),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('issue_date', sa.Date(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('amount > 0', name='check_amount_positive'),
        sa.CheckConstraint("status IN ('pending', 'paid', 'overdue', 'cancelled')", name='check_status_valid'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoices_user_id'), 'invoices', ['user_id'], unique=False)
    op.create_index(op.f('ix_invoices_invoice_number'), 'invoices', ['invoice_number'], unique=False)
    op.create_index(op.f('ix_invoices_client_name'), 'invoices', ['client_name'], unique=False)
    op.create_index(op.f('ix_invoices_issue_date'), 'invoices', ['issue_date'], unique=False)
    op.create_index(op.f('ix_invoices_due_date'), 'invoices', ['due_date'], unique=False)
    op.create_index(op.f('ix_invoices_payment_date'), 'invoices', ['payment_date'], unique=False)
    op.create_index(op.f('ix_invoices_status'), 'invoices', ['status'], unique=False)

    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bank_account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bridge_transaction_id', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('is_recurring', sa.Boolean(), nullable=True),
        sa.Column('is_reconciled', sa.Boolean(), nullable=True),
        sa.Column('reconciled_invoice_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('raw_data', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint('amount != 0', name='check_amount_not_zero'),
        sa.ForeignKeyConstraint(['bank_account_id'], ['bank_accounts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('bridge_transaction_id')
    )
    op.create_index(op.f('ix_transactions_bank_account_id'), 'transactions', ['bank_account_id'], unique=False)
    op.create_index(op.f('ix_transactions_bridge_transaction_id'), 'transactions', ['bridge_transaction_id'], unique=True)
    op.create_index(op.f('ix_transactions_date'), 'transactions', ['date'], unique=False)
    op.create_index(op.f('ix_transactions_category'), 'transactions', ['category'], unique=False)
    op.create_index(op.f('ix_transactions_is_reconciled'), 'transactions', ['is_reconciled'], unique=False)
    op.create_index(op.f('ix_transactions_reconciled_invoice_id'), 'transactions', ['reconciled_invoice_id'], unique=False)

    # Create reminders table
    op.create_table(
        'reminders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reminder_type', sa.String(length=50), nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('email_subject', sa.String(length=255), nullable=True),
        sa.Column('email_body', sa.Text(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reminders_invoice_id'), 'reminders', ['invoice_id'], unique=False)
    op.create_index(op.f('ix_reminders_scheduled_at'), 'reminders', ['scheduled_at'], unique=False)
    op.create_index(op.f('ix_reminders_sent_at'), 'reminders', ['sent_at'], unique=False)
    op.create_index(op.f('ix_reminders_status'), 'reminders', ['status'], unique=False)

    # Create reconciliations table
    op.create_table(
        'reconciliations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('transaction_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('confidence_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('match_type', sa.String(length=50), nullable=False),
        sa.Column('is_validated', sa.Boolean(), nullable=True),
        sa.Column('validated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ai_reasoning', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_id')
    )
    op.create_index(op.f('ix_reconciliations_transaction_id'), 'reconciliations', ['transaction_id'], unique=True)
    op.create_index(op.f('ix_reconciliations_invoice_id'), 'reconciliations', ['invoice_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_reconciliations_invoice_id'), table_name='reconciliations')
    op.drop_index(op.f('ix_reconciliations_transaction_id'), table_name='reconciliations')
    op.drop_table('reconciliations')

    op.drop_index(op.f('ix_reminders_status'), table_name='reminders')
    op.drop_index(op.f('ix_reminders_sent_at'), table_name='reminders')
    op.drop_index(op.f('ix_reminders_scheduled_at'), table_name='reminders')
    op.drop_index(op.f('ix_reminders_invoice_id'), table_name='reminders')
    op.drop_table('reminders')

    op.drop_index(op.f('ix_transactions_reconciled_invoice_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_is_reconciled'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_category'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_date'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_bridge_transaction_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_bank_account_id'), table_name='transactions')
    op.drop_table('transactions')

    op.drop_index(op.f('ix_invoices_status'), table_name='invoices')
    op.drop_index(op.f('ix_invoices_payment_date'), table_name='invoices')
    op.drop_index(op.f('ix_invoices_due_date'), table_name='invoices')
    op.drop_index(op.f('ix_invoices_issue_date'), table_name='invoices')
    op.drop_index(op.f('ix_invoices_client_name'), table_name='invoices')
    op.drop_index(op.f('ix_invoices_invoice_number'), table_name='invoices')
    op.drop_index(op.f('ix_invoices_user_id'), table_name='invoices')
    op.drop_table('invoices')

    op.drop_index(op.f('ix_bank_accounts_bridge_item_id'), table_name='bank_accounts')
    op.drop_index(op.f('ix_bank_accounts_bridge_account_id'), table_name='bank_accounts')
    op.drop_index(op.f('ix_bank_accounts_user_id'), table_name='bank_accounts')
    op.drop_table('bank_accounts')

    op.drop_index(op.f('ix_audit_logs_created_at'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_entity_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_entity_type'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    op.drop_table('audit_logs')


