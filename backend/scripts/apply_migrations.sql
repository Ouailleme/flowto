-- Apply all business models migration
-- Create audit_logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS ix_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS ix_audit_logs_entity_type ON audit_logs(entity_type);
CREATE INDEX IF NOT EXISTS ix_audit_logs_entity_id ON audit_logs(entity_id);
CREATE INDEX IF NOT EXISTS ix_audit_logs_created_at ON audit_logs(created_at);

-- Create bank_accounts table
CREATE TABLE IF NOT EXISTS bank_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bridge_account_id VARCHAR(255) UNIQUE NOT NULL,
    bridge_item_id VARCHAR(255) NOT NULL,
    bank_name VARCHAR(255) NOT NULL,
    account_name VARCHAR(255),
    account_type VARCHAR(50),
    iban VARCHAR(100),
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_bank_accounts_user_id ON bank_accounts(user_id);
CREATE INDEX IF NOT EXISTS ix_bank_accounts_bridge_account_id ON bank_accounts(bridge_account_id);
CREATE INDEX IF NOT EXISTS ix_bank_accounts_bridge_item_id ON bank_accounts(bridge_item_id);

-- Create invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    invoice_number VARCHAR(50) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255),
    amount NUMERIC(15, 2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    payment_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'overdue', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_invoices_user_id ON invoices(user_id);
CREATE INDEX IF NOT EXISTS ix_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS ix_invoices_client_name ON invoices(client_name);
CREATE INDEX IF NOT EXISTS ix_invoices_issue_date ON invoices(issue_date);
CREATE INDEX IF NOT EXISTS ix_invoices_due_date ON invoices(due_date);
CREATE INDEX IF NOT EXISTS ix_invoices_payment_date ON invoices(payment_date);
CREATE INDEX IF NOT EXISTS ix_invoices_status ON invoices(status);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bank_account_id UUID NOT NULL REFERENCES bank_accounts(id) ON DELETE CASCADE,
    bridge_transaction_id VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC(15, 2) NOT NULL CHECK (amount != 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    date TIMESTAMPTZ NOT NULL,
    category VARCHAR(100),
    is_recurring BOOLEAN DEFAULT FALSE,
    is_reconciled BOOLEAN DEFAULT FALSE,
    reconciled_invoice_id UUID,
    raw_data TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_transactions_bank_account_id ON transactions(bank_account_id);
CREATE INDEX IF NOT EXISTS ix_transactions_bridge_transaction_id ON transactions(bridge_transaction_id);
CREATE INDEX IF NOT EXISTS ix_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS ix_transactions_category ON transactions(category);
CREATE INDEX IF NOT EXISTS ix_transactions_is_reconciled ON transactions(is_reconciled);
CREATE INDEX IF NOT EXISTS ix_transactions_reconciled_invoice_id ON transactions(reconciled_invoice_id);

-- Create reminders table
CREATE TABLE IF NOT EXISTS reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    reminder_type VARCHAR(50) NOT NULL,
    scheduled_at TIMESTAMPTZ NOT NULL,
    sent_at TIMESTAMPTZ,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    email_subject VARCHAR(255),
    email_body TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_reminders_invoice_id ON reminders(invoice_id);
CREATE INDEX IF NOT EXISTS ix_reminders_scheduled_at ON reminders(scheduled_at);
CREATE INDEX IF NOT EXISTS ix_reminders_sent_at ON reminders(sent_at);
CREATE INDEX IF NOT EXISTS ix_reminders_status ON reminders(status);

-- Create reconciliations table
CREATE TABLE IF NOT EXISTS reconciliations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID UNIQUE NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    confidence_score NUMERIC(5, 2) NOT NULL,
    match_type VARCHAR(50) NOT NULL,
    is_validated BOOLEAN DEFAULT FALSE,
    validated_by UUID,
    validated_at TIMESTAMPTZ,
    ai_reasoning TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_reconciliations_transaction_id ON reconciliations(transaction_id);
CREATE INDEX IF NOT EXISTS ix_reconciliations_invoice_id ON reconciliations(invoice_id);


