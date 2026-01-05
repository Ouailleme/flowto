-- FinanceAI - Database initialization script
-- This script creates all tables and inserts demo data

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    language VARCHAR(10) DEFAULT 'fr',
    country VARCHAR(10) DEFAULT 'FR',
    currency VARCHAR(10) DEFAULT 'EUR',
    timezone VARCHAR(50) DEFAULT 'Europe/Paris',
    locale VARCHAR(20) DEFAULT 'fr_FR',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create bank_accounts table
CREATE TABLE IF NOT EXISTS bank_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bank_name VARCHAR(255) NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    account_number VARCHAR(255),
    currency VARCHAR(10) NOT NULL DEFAULT 'EUR',
    balance NUMERIC(12, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMPTZ,
    bridge_item_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bank_account_id UUID NOT NULL REFERENCES bank_accounts(id) ON DELETE CASCADE,
    description VARCHAR(500) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'EUR',
    transaction_date TIMESTAMPTZ NOT NULL,
    category VARCHAR(100),
    is_reconciled BOOLEAN DEFAULT FALSE,
    amount_converted NUMERIC(12, 2),
    conversion_rate NUMERIC(12, 6),
    converted_currency VARCHAR(10),
    bridge_transaction_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_name VARCHAR(255) NOT NULL,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'EUR',
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    pdf_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create reconciliations table
CREATE TABLE IF NOT EXISTS reconciliations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    transaction_id UUID NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    confidence_score NUMERIC(5, 2),
    reconciliation_date TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create reminders table
CREATE TABLE IF NOT EXISTS reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    reminder_type VARCHAR(50) NOT NULL,
    sent_at TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create audit_logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_bank_accounts_user_id ON bank_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_bank_account_id ON transactions(bank_account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_invoices_user_id ON invoices(user_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_reconciliations_transaction_id ON reconciliations(transaction_id);
CREATE INDEX IF NOT EXISTS idx_reconciliations_invoice_id ON reconciliations(invoice_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs(entity_type, entity_id);

-- Insert demo user (password: demo123, hashed with bcrypt)
INSERT INTO users (id, email, hashed_password, full_name, is_active, is_verified, language, country, currency, timezone, locale)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'demo@financeai.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5etzKFpkGvVKa', -- demo123
    'Demo User',
    TRUE,
    TRUE,
    'fr',
    'FR',
    'EUR',
    'Europe/Paris',
    'fr_FR'
) ON CONFLICT (email) DO NOTHING;

-- Insert demo bank account
INSERT INTO bank_accounts (id, user_id, bank_name, account_name, account_number, currency, balance, last_sync)
VALUES (
    'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'BNP Paribas',
    'Compte Courant',
    'FR7630006000011234567890189',
    'EUR',
    15420.50,
    NOW()
) ON CONFLICT DO NOTHING;

-- Insert demo transactions
INSERT INTO transactions (user_id, bank_account_id, description, amount, currency, transaction_date, category)
VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Loyer Bureau', -1200.00, 'EUR', NOW() - INTERVAL '5 days', 'Charges fixes'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Vente Client A', 2500.00, 'EUR', NOW() - INTERVAL '3 days', 'Revenus'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Fournitures Bureau', -85.75, 'EUR', NOW() - INTERVAL '7 days', 'Dépenses de bureau'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Salaires', -3500.00, 'EUR', NOW() - INTERVAL '10 days', 'Charges de personnel'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Vente Client B', 1800.00, 'EUR', NOW() - INTERVAL '2 days', 'Revenus'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Marketing Digital', -300.00, 'EUR', NOW() - INTERVAL '12 days', 'Marketing'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Déjeuner Affaires', -75.20, 'EUR', NOW() - INTERVAL '1 day', 'Frais professionnels'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Maintenance Logiciel', -150.00, 'EUR', NOW() - INTERVAL '8 days', 'Services IT'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Vente Client C', 900.00, 'EUR', NOW() - INTERVAL '4 days', 'Revenus')
ON CONFLICT DO NOTHING;

-- Insert demo invoices
INSERT INTO invoices (user_id, client_name, invoice_number, amount, currency, issue_date, due_date, status)
VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Client Alpha', 'INV-0001', 1200.00, 'EUR', NOW() - INTERVAL '20 days', NOW() - INTERVAL '10 days', 'paid'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Client Beta', 'INV-0002', 850.00, 'EUR', NOW() - INTERVAL '10 days', NOW() + INTERVAL '5 days', 'pending'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Client Gamma', 'INV-0003', 2100.00, 'EUR', NOW() - INTERVAL '30 days', NOW() - INTERVAL '20 days', 'overdue'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Client Delta', 'INV-0004', 450.00, 'EUR', NOW() - INTERVAL '5 days', NOW() - INTERVAL '3 days', 'paid'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Client Epsilon', 'INV-0005', 1500.00, 'EUR', NOW() - INTERVAL '3 days', NOW() + INTERVAL '15 days', 'pending')
ON CONFLICT (invoice_number) DO NOTHING;

-- Success message
\echo '✅ Database initialized successfully!'
\echo '📊 Tables created'
\echo '👤 Demo user: demo@financeai.com / demo123'
\echo '🏦 Demo data inserted'


