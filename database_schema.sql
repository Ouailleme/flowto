-- FinanceAI Database Schema
-- PostgreSQL 16+
-- À exécuter dans Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable Row Level Security
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-jwt-secret-here';

---------------------------------------------------
-- TABLES
---------------------------------------------------

-- Users (extends Supabase auth.users)
CREATE TABLE public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    company_name VARCHAR(255),
    company_size VARCHAR(50),
    subscription_plan VARCHAR(50) DEFAULT 'trial',
    subscription_status VARCHAR(50) DEFAULT 'active',
    trial_ends_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '14 days'),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bank Accounts
CREATE TABLE public.bank_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    bridge_account_id VARCHAR(255) UNIQUE,
    bank_name VARCHAR(255),
    account_type VARCHAR(50),
    iban VARCHAR(50),
    balance DECIMAL(15,2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'EUR',
    is_active BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Transactions
CREATE TABLE public.transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bank_account_id UUID NOT NULL REFERENCES public.bank_accounts(id) ON DELETE CASCADE,
    bridge_transaction_id VARCHAR(255) UNIQUE,
    date DATE NOT NULL,
    description TEXT,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    category VARCHAR(100),
    category_confidence DECIMAL(3,2),
    is_reconciled BOOLEAN DEFAULT false,
    reconciliation_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Invoices
CREATE TABLE public.invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    invoice_number VARCHAR(100),
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255),
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    payment_date DATE,
    is_reconciled BOOLEAN DEFAULT false,
    reconciliation_id UUID,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT check_amount_positive CHECK (amount > 0),
    CONSTRAINT check_status_valid CHECK (status IN ('pending', 'paid', 'overdue', 'cancelled')),
    CONSTRAINT check_due_after_issue CHECK (due_date >= issue_date)
);

-- Reconciliations
CREATE TABLE public.reconciliations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    transaction_id UUID REFERENCES public.transactions(id) ON DELETE CASCADE,
    invoice_id UUID REFERENCES public.invoices(id) ON DELETE CASCADE,
    match_score DECIMAL(3,2),
    match_method VARCHAR(50),
    validated_by VARCHAR(50),
    validated_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT check_match_score_range CHECK (match_score >= 0 AND match_score <= 1),
    CONSTRAINT check_match_method_valid CHECK (match_method IN ('exact', 'reference', 'fuzzy_ai', 'manual'))
);

-- Reminders (Relances)
CREATE TABLE public.reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID NOT NULL REFERENCES public.invoices(id) ON DELETE CASCADE,
    sent_at TIMESTAMPTZ NOT NULL,
    reminder_type VARCHAR(50) NOT NULL,
    email_subject TEXT,
    email_body TEXT,
    opened_at TIMESTAMPTZ,
    clicked_at TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'sent',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT check_reminder_type_valid CHECK (reminder_type IN ('first', 'second', 'final'))
);

-- Cash Flow Forecasts
CREATE TABLE public.forecasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    forecast_date DATE NOT NULL,
    predicted_balance DECIMAL(15,2),
    confidence_level VARCHAR(50),
    scenario VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT check_scenario_valid CHECK (scenario IN ('conservative', 'realistic', 'optimistic'))
);

-- Audit Logs
CREATE TABLE public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

---------------------------------------------------
-- INDEXES
---------------------------------------------------

-- Bank Accounts
CREATE INDEX idx_bank_accounts_user ON public.bank_accounts(user_id);
CREATE INDEX idx_bank_accounts_active ON public.bank_accounts(user_id, is_active);

-- Transactions
CREATE INDEX idx_transactions_bank_account ON public.transactions(bank_account_id);
CREATE INDEX idx_transactions_date ON public.transactions(date DESC);
CREATE INDEX idx_transactions_bridge_id ON public.transactions(bridge_transaction_id);
CREATE INDEX idx_transactions_reconciled ON public.transactions(is_reconciled);

-- Invoices
CREATE INDEX idx_invoices_user ON public.invoices(user_id);
CREATE INDEX idx_invoices_status ON public.invoices(user_id, status);
CREATE INDEX idx_invoices_due_date ON public.invoices(due_date);
CREATE INDEX idx_invoices_client ON public.invoices(user_id, client_name);

-- Reconciliations
CREATE INDEX idx_reconciliations_transaction ON public.reconciliations(transaction_id);
CREATE INDEX idx_reconciliations_invoice ON public.reconciliations(invoice_id);
CREATE INDEX idx_reconciliations_user ON public.reconciliations(user_id);

-- Reminders
CREATE INDEX idx_reminders_invoice ON public.reminders(invoice_id);
CREATE INDEX idx_reminders_sent ON public.reminders(sent_at DESC);

-- Forecasts
CREATE INDEX idx_forecasts_user_date ON public.forecasts(user_id, forecast_date DESC);

-- Audit Logs
CREATE INDEX idx_audit_logs_user ON public.audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_logs_entity ON public.audit_logs(entity_type, entity_id);

---------------------------------------------------
-- FUNCTIONS & TRIGGERS
---------------------------------------------------

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bank_accounts_updated_at
    BEFORE UPDATE ON public.bank_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at
    BEFORE UPDATE ON public.transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_invoices_updated_at
    BEFORE UPDATE ON public.invoices
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function: Update invoice status based on due_date
CREATE OR REPLACE FUNCTION update_invoice_status()
RETURNS void AS $$
BEGIN
    UPDATE public.invoices
    SET status = 'overdue'
    WHERE status = 'pending'
    AND due_date < CURRENT_DATE;
END;
$$ LANGUAGE plpgsql;

-- Function: Link reconciliation IDs
CREATE OR REPLACE FUNCTION link_reconciliation()
RETURNS TRIGGER AS $$
BEGIN
    -- Update transaction
    IF NEW.transaction_id IS NOT NULL THEN
        UPDATE public.transactions
        SET is_reconciled = true,
            reconciliation_id = NEW.id
        WHERE id = NEW.transaction_id;
    END IF;
    
    -- Update invoice
    IF NEW.invoice_id IS NOT NULL THEN
        UPDATE public.invoices
        SET is_reconciled = true,
            reconciliation_id = NEW.id,
            status = 'paid',
            payment_date = (
                SELECT date FROM public.transactions 
                WHERE id = NEW.transaction_id
            )
        WHERE id = NEW.invoice_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_reconciliation_insert
    AFTER INSERT ON public.reconciliations
    FOR EACH ROW
    EXECUTE FUNCTION link_reconciliation();

---------------------------------------------------
-- ROW LEVEL SECURITY (RLS)
---------------------------------------------------

-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bank_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reconciliations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.forecasts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies: Users can only access their own data

-- Users
CREATE POLICY users_select_own ON public.users
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY users_update_own ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- Bank Accounts
CREATE POLICY bank_accounts_select_own ON public.bank_accounts
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY bank_accounts_insert_own ON public.bank_accounts
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY bank_accounts_update_own ON public.bank_accounts
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY bank_accounts_delete_own ON public.bank_accounts
    FOR DELETE USING (auth.uid() = user_id);

-- Transactions
CREATE POLICY transactions_select_own ON public.transactions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.bank_accounts
            WHERE bank_accounts.id = transactions.bank_account_id
            AND bank_accounts.user_id = auth.uid()
        )
    );

-- Invoices
CREATE POLICY invoices_select_own ON public.invoices
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY invoices_insert_own ON public.invoices
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY invoices_update_own ON public.invoices
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY invoices_delete_own ON public.invoices
    FOR DELETE USING (auth.uid() = user_id);

-- Reconciliations
CREATE POLICY reconciliations_select_own ON public.reconciliations
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY reconciliations_insert_own ON public.reconciliations
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY reconciliations_update_own ON public.reconciliations
    FOR UPDATE USING (auth.uid() = user_id);

-- Reminders
CREATE POLICY reminders_select_own ON public.reminders
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.invoices
            WHERE invoices.id = reminders.invoice_id
            AND invoices.user_id = auth.uid()
        )
    );

-- Forecasts
CREATE POLICY forecasts_select_own ON public.forecasts
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY forecasts_insert_own ON public.forecasts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Audit Logs
CREATE POLICY audit_logs_select_own ON public.audit_logs
    FOR SELECT USING (auth.uid() = user_id);

---------------------------------------------------
-- INITIAL DATA (Optional)
---------------------------------------------------

-- Categories for transaction categorization
CREATE TABLE IF NOT EXISTS public.transaction_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO public.transaction_categories (name, description, icon) VALUES
    ('Salaires', 'Paiements salaires et charges sociales', '💼'),
    ('Fournitures', 'Achats fournitures et matériel', '📦'),
    ('Loyer', 'Loyer et charges locatives', '🏢'),
    ('Clients', 'Paiements clients', '💰'),
    ('Banque', 'Frais bancaires et intérêts', '🏦'),
    ('Taxes', 'Impôts et taxes', '📊'),
    ('Marketing', 'Dépenses marketing et publicité', '📣'),
    ('Transport', 'Frais de déplacement', '🚗'),
    ('Abonnements', 'Abonnements logiciels et services', '💻'),
    ('Autre', 'Autres dépenses', '📌')
ON CONFLICT (name) DO NOTHING;

---------------------------------------------------
-- VIEWS (Useful queries)
---------------------------------------------------

-- View: Dashboard Summary
CREATE OR REPLACE VIEW public.dashboard_summary AS
SELECT 
    u.id as user_id,
    COALESCE(SUM(ba.balance), 0) as total_balance,
    COUNT(DISTINCT ba.id) as bank_accounts_count,
    COUNT(DISTINCT CASE WHEN i.status = 'pending' THEN i.id END) as pending_invoices_count,
    COALESCE(SUM(CASE WHEN i.status = 'pending' THEN i.amount ELSE 0 END), 0) as pending_invoices_amount,
    COUNT(DISTINCT CASE WHEN r.validated_at IS NULL THEN r.id END) as pending_reconciliations_count
FROM public.users u
LEFT JOIN public.bank_accounts ba ON ba.user_id = u.id AND ba.is_active = true
LEFT JOIN public.invoices i ON i.user_id = u.id
LEFT JOIN public.reconciliations r ON r.user_id = u.id
GROUP BY u.id;

-- View: Recent Transactions
CREATE OR REPLACE VIEW public.recent_transactions AS
SELECT 
    t.id,
    t.date,
    t.description,
    t.amount,
    t.category,
    t.is_reconciled,
    ba.bank_name,
    ba.user_id
FROM public.transactions t
JOIN public.bank_accounts ba ON ba.id = t.bank_account_id
ORDER BY t.date DESC, t.created_at DESC;

---------------------------------------------------
-- GRANTS (Permissions)
---------------------------------------------------

-- Grant authenticated users access to their data
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

---------------------------------------------------
-- COMMENTS
---------------------------------------------------

COMMENT ON TABLE public.users IS 'Utilisateurs de l''application (entreprises PME)';
COMMENT ON TABLE public.bank_accounts IS 'Comptes bancaires connectés via Bridge API';
COMMENT ON TABLE public.transactions IS 'Transactions bancaires synchronisées';
COMMENT ON TABLE public.invoices IS 'Factures clients à rapprocher';
COMMENT ON TABLE public.reconciliations IS 'Rapprochements transactions ↔ factures';
COMMENT ON TABLE public.reminders IS 'Historique des relances envoyées';
COMMENT ON TABLE public.forecasts IS 'Prévisions de trésorerie générées par IA';
COMMENT ON TABLE public.audit_logs IS 'Journal d''audit de toutes les actions';

---------------------------------------------------
-- COMPLETION
---------------------------------------------------

-- Verify installation
DO $$
BEGIN
    RAISE NOTICE '✅ FinanceAI database schema installed successfully!';
    RAISE NOTICE 'Tables created: users, bank_accounts, transactions, invoices, reconciliations, reminders, forecasts, audit_logs';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Update JWT secret in ALTER DATABASE command';
    RAISE NOTICE '2. Test with: SELECT * FROM public.transaction_categories;';
    RAISE NOTICE '3. Create first user via Supabase Auth';
END $$;


