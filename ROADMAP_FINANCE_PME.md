# ROADMAP TECHNIQUE - Automatisation Finance PME

## 🎯 Vision Produit

**Nom**: FinanceAI (nom de travail)
**Tagline**: "Automatisez votre comptabilité PME en 30 minutes"
**Mission**: Libérer les PME des tâches comptables répétitives via IA

---

## 📅 TIMELINE GLOBALE

**Phase 1**: MVP No-Code (Semaines 1-8) → Validation PMF
**Phase 2**: Migration Code (Semaines 9-20) → Scaling 100+ clients
**Phase 3**: Scale & Enterprise Features (Mois 6-12) → 500+ clients

---

## PHASE 1: MVP NO-CODE (8 SEMAINES)

### 🎯 Objectif: Validation Product-Market Fit avec 20-30 clients payants

### Sprint 0: Setup & Validation (Semaines 1-2)

#### Semaine 1: Pre-Development
**Objectifs**:
- ✅ Validation finale niche (interviews + landing page)
- ✅ Setup infrastructure de base
- ✅ Création entité légale

**Livrables**:
- [ ] 30+ emails waitlist
- [ ] 15+ interviews complétées
- [ ] 5+ pre-sales confirmées
- [ ] SASU/SAS créée
- [ ] Comptes bancaires ouverts (business + Stripe)
- [ ] Domaines achetés (financeai.fr + alternatives)

**Tâches Techniques**:
```bash
# Infrastructure
- Acheter domaine financeai.fr
- Setup email professionnel (Google Workspace 6€/mois)
- Créer comptes:
  - Stripe (paiements)
  - Bubble.io (frontend)
  - Make.com (workflows)
  - Supabase (database)
  - Bridge API (banking)
  - Anthropic (Claude API)
  - SendGrid (emails)
```

#### Semaine 2: Architecture & Design
**Objectifs**:
- ✅ Définir architecture détaillée
- ✅ Créer mockups UX/UI
- ✅ Setup environnements dev/prod

**Livrables**:
- [ ] Architecture diagram (Excalidraw/Figma)
- [ ] Mockups 8 écrans principaux (Figma)
- [ ] Database schema v1
- [ ] API contracts définis
- [ ] Environnements séparés (dev/prod)

**Database Schema v1** (Supabase):
```sql
-- Users & Auth
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  company_name VARCHAR(255),
  company_size VARCHAR(50),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  subscription_plan VARCHAR(50),
  subscription_status VARCHAR(50),
  trial_ends_at TIMESTAMPTZ
);

-- Bank Accounts
CREATE TABLE bank_accounts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  bridge_account_id VARCHAR(255) UNIQUE,
  bank_name VARCHAR(255),
  account_type VARCHAR(50),
  iban VARCHAR(50),
  balance DECIMAL(15,2),
  currency VARCHAR(3) DEFAULT 'EUR',
  is_active BOOLEAN DEFAULT true,
  last_sync_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Transactions
CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  bank_account_id UUID REFERENCES bank_accounts(id) ON DELETE CASCADE,
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
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  invoice_number VARCHAR(100),
  client_name VARCHAR(255),
  client_email VARCHAR(255),
  amount DECIMAL(15,2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'EUR',
  issue_date DATE NOT NULL,
  due_date DATE NOT NULL,
  status VARCHAR(50), -- pending, paid, overdue, cancelled
  payment_date DATE,
  is_reconciled BOOLEAN DEFAULT false,
  reconciliation_id UUID,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reconciliations
CREATE TABLE reconciliations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  transaction_id UUID REFERENCES transactions(id),
  invoice_id UUID REFERENCES invoices(id),
  match_score DECIMAL(3,2), -- 0.00 to 1.00
  match_method VARCHAR(50), -- exact, fuzzy, manual
  validated_by VARCHAR(50), -- ai, user
  validated_at TIMESTAMPTZ,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reminders (Relances)
CREATE TABLE reminders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
  sent_at TIMESTAMPTZ NOT NULL,
  reminder_type VARCHAR(50), -- first, second, final
  email_subject TEXT,
  email_body TEXT,
  opened_at TIMESTAMPTZ,
  clicked_at TIMESTAMPTZ,
  status VARCHAR(50), -- sent, opened, clicked, replied
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cash Flow Forecasts
CREATE TABLE forecasts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  forecast_date DATE NOT NULL,
  predicted_balance DECIMAL(15,2),
  confidence_level VARCHAR(50),
  scenario VARCHAR(50), -- conservative, realistic, optimistic
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit Logs
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  action VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50),
  entity_id UUID,
  old_values JSONB,
  new_values JSONB,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_transactions_bank_account ON transactions(bank_account_id);
CREATE INDEX idx_transactions_date ON transactions(date DESC);
CREATE INDEX idx_invoices_user_status ON invoices(user_id, status);
CREATE INDEX idx_invoices_due_date ON invoices(due_date);
CREATE INDEX idx_reconciliations_transaction ON reconciliations(transaction_id);
CREATE INDEX idx_reconciliations_invoice ON reconciliations(invoice_id);
CREATE INDEX idx_audit_logs_user_created ON audit_logs(user_id, created_at DESC);
```

### Sprint 1: Core Banking Integration (Semaines 3-4)

#### Semaine 3: Bridge API Integration
**Objectifs**:
- ✅ Intégrer Bridge API (agrégateur bancaire DSP2)
- ✅ Créer flow onboarding bancaire
- ✅ Sync transactions automatique

**Tâches Make.com**:

**Workflow 1: Bank Connection**
```
Trigger: Bubble.io webhook (user initiates bank connection)
│
├─ Bridge API: Generate connect URL
├─ Return URL to Bubble
├─ User completes OAuth flow (external)
├─ Bridge webhook: connection successful
├─ Store bank_account in Supabase
│  ├─ bridge_account_id
│  ├─ bank_name
│  ├─ iban
│  └─ user_id
│
└─ Trigger initial sync (Workflow 2)
```

**Workflow 2: Sync Transactions (Daily Cron)**
```
Trigger: Scheduled (6:00 AM daily)
│
├─ Get all active bank_accounts (Supabase)
│
├─ For each account:
│  ├─ Bridge API: Get transactions (last 90 days)
│  ├─ Deduplicate (check bridge_transaction_id)
│  │
│  ├─ For each new transaction:
│  │  ├─ Claude API: Categorize transaction
│  │  │  Prompt: "Categorize this transaction:
│  │  │           Description: {description}
│  │  │           Amount: {amount}
│  │  │           Categories: [Salaires, Fournitures, Loyer, 
│  │  │                        Clients, Banque, Taxes, Autre]
│  │  │           Return JSON: {category, confidence}"
│  │  │
│  │  ├─ Insert transaction in Supabase
│  │  │  ├─ description
│  │  │  ├─ amount
│  │  │  ├─ date
│  │  │  ├─ category
│  │  │  └─ category_confidence
│  │  │
│  │  └─ Trigger reconciliation check (Workflow 3)
│  │
│  └─ Update last_sync_at
│
└─ Send summary email (if new transactions)
```

**Livrables**:
- [ ] Bridge API integration complète
- [ ] 3 banques françaises testées minimum
- [ ] Workflow sync fonctionnel
- [ ] Catégorisation IA 80%+ précision
- [ ] Dashboard transactions basique (Bubble)

#### Semaine 4: Reconciliation Engine
**Objectifs**:
- ✅ Créer moteur de rapprochement automatique
- ✅ UI validation rapprochements
- ✅ Export comptable

**Workflow 3: Auto-Reconciliation**
```
Trigger: New transaction inserted OR New invoice created
│
├─ Get all unpaid invoices for user
│
├─ Matching Algorithm (3 levels):
│
│  1. EXACT MATCH:
│     ├─ Amount exact (±0.01€)
│     ├─ Date ±3 days
│     └─ Score: 1.00
│
│  2. REFERENCE MATCH:
│     ├─ Invoice number in description (regex)
│     ├─ Amount exact
│     └─ Score: 0.95
│
│  3. FUZZY MATCH (Claude AI):
│     Prompt: "Match this transaction to invoice:
│              Transaction: {description} - {amount}€ on {date}
│              Invoice: {client_name} - {amount}€ due {due_date}
│              Ref: {invoice_number}
│              
│              Return JSON: {
│                match_probability: 0.0-1.0,
│                reasoning: string
│              }"
│     └─ Score: Claude output
│
├─ If score >= 0.80:
│  ├─ Create reconciliation (auto-validated)
│  ├─ Mark transaction as reconciled
│  ├─ Mark invoice as paid
│  └─ Send confirmation email
│
├─ If score 0.50-0.79:
│  ├─ Create reconciliation (pending validation)
│  └─ Notify user (dashboard + email)
│
└─ If score < 0.50:
   └─ No action (manual only)
```

**Livrables**:
- [ ] Moteur de matching fonctionnel
- [ ] UI validation suggestions
- [ ] Tests: 50 transactions réelles, 90%+ précision
- [ ] Export CSV compatible Pennylane/Sage

### Sprint 2: Invoice Management & Reminders (Semaines 5-6)

#### Semaine 5: Invoice Import & Management
**Objectifs**:
- ✅ Import factures (CSV/intégration Pennylane)
- ✅ CRUD factures manuel
- ✅ Dashboard factures

**Tâches Bubble.io**:
```
Pages:
1. Invoices List
   - Table: invoice_number, client, amount, due_date, status
   - Filters: status, date range
   - Actions: Edit, Delete, Create Reminder

2. Invoice Detail/Edit
   - Form: tous champs
   - History: reconciliations, reminders
   - Actions: Mark Paid, Send Reminder

3. Invoice Import
   - CSV upload
   - Mapping columns
   - Preview + Validate
   - Bulk insert
```

**Workflow 4: Pennylane Integration** (si demandé)
```
Trigger: Scheduled (daily) OR Manual
│
├─ Pennylane API: Get invoices (last 90 days)
│
├─ For each invoice:
│  ├─ Check if exists (invoice_number)
│  ├─ If new: Insert Supabase
│  └─ If updated: Update Supabase
│
└─ Trigger reconciliation checks
```

#### Semaine 6: Automated Reminders
**Objectifs**:
- ✅ Génération emails relances (IA)
- ✅ Envoi automatique selon règles
- ✅ Tracking ouvertures

**Workflow 5: Reminder Generation & Sending**
```
Trigger: Scheduled (Monday 9:00 AM)
│
├─ Get all overdue invoices (due_date < today AND status = pending)
│
├─ For each invoice:
│  ├─ Check reminder history:
│  │  - Last reminder sent? (avoid spam)
│  │  - Number of reminders? (escalation)
│  │
│  ├─ Determine reminder type:
│  │  - First: +7 days overdue (courteous)
│  │  - Second: +21 days (firmer)
│  │  - Final: +45 days (formal)
│  │
│  ├─ Claude API: Generate personalized email
│  │  Prompt: "Generate a {reminder_type} reminder email:
│  │           Client: {client_name}
│  │           Invoice: {invoice_number} - {amount}€
│  │           Due date: {due_date} ({days_overdue} days ago)
│  │           Tone: {courteous/firm/formal}
│  │           
│  │           Return JSON: {
│  │             subject: string,
│  │             body: string (HTML)
│  │           }"
│  │
│  ├─ SendGrid API: Send email
│  │  - From: {user_company}@financeai.fr (custom domain)
│  │  - To: {client_email}
│  │  - Subject: {subject}
│  │  - Body: {body}
│  │  - Track opens/clicks
│  │
│  ├─ Store reminder in database
│  │
│  └─ Increment invoice reminder_count
│
└─ Send summary to user (X reminders sent)
```

**Livrables**:
- [ ] Import CSV factures fonctionnel
- [ ] Intégration Pennylane (optionnel)
- [ ] Génération emails IA (3 tons)
- [ ] Envoi automatique + tracking
- [ ] Tests: 20 relances générées, qualité vérifiée

### Sprint 3: Dashboard & Forecasting (Semaines 7-8)

#### Semaine 7: Dashboard & Analytics
**Objectifs**:
- ✅ Dashboard trésorerie
- ✅ Graphiques évolution
- ✅ Indicateurs clés

**Pages Bubble.io**:
```
1. Dashboard (Homepage)
   
   KPIs (Top):
   - Solde bancaire actuel
   - Factures en attente (montant)
   - Trésorerie prévue 30j
   - Réconciliations à valider
   
   Charts:
   - Évolution trésorerie (line chart, 6 mois)
   - Répartition dépenses par catégorie (pie chart)
   - Factures payées vs en attente (bar chart)
   
   Recent Activity:
   - Dernières transactions (5)
   - Dernières réconciliations (5)
   - Prochaines échéances (5)
   
   Quick Actions:
   - Ajouter facture
   - Sync banques
   - Envoyer relances
```

#### Semaine 8: Cash Flow Forecasting
**Objectifs**:
- ✅ Prévisions trésorerie 3 mois
- ✅ Scénarios (optimiste/réaliste/pessimiste)
- ✅ Alertes seuils

**Workflow 6: Forecast Generation**
```
Trigger: Manual OR Scheduled (weekly)
│
├─ Get historical data (6 months):
│  ├─ Transactions by category
│  ├─ Invoice payment patterns
│  └─ Balance evolution
│
├─ Claude API: Generate forecast
│  Prompt: "Generate 3-month cash flow forecast:
│           
│           Current balance: {balance}€
│           
│           Historical data:
│           - Monthly revenue (avg): {avg_revenue}€
│           - Monthly expenses (avg): {avg_expenses}€
│           - Expense breakdown: {categories}
│           - Payment delays (avg): {avg_delay} days
│           
│           Pending invoices:
│           {invoices_list}
│           
│           Generate 3 scenarios (conservative, realistic, optimistic):
│           For each month (M+1, M+2, M+3), predict:
│           - Expected revenue
│           - Expected expenses
│           - End-of-month balance
│           - Confidence level
│           
│           Return JSON"
│
├─ Store forecasts in database
│
├─ If any month < threshold (e.g., 5000€):
│  └─ Send alert to user
│
└─ Display in dashboard
```

**Livrables**:
- [ ] Dashboard complet et responsive
- [ ] 5 charts interactifs
- [ ] Prévisions 3 mois fonctionnelles
- [ ] Alertes trésorerie configurables
- [ ] **MVP v1.0 COMPLET** ✅

---

## PHASE 2: MIGRATION CODE (12 SEMAINES)

### 🎯 Objectif: Architecture scalable pour 100-500 clients

**Trigger Migration**: 
- 30+ clients actifs
- MRR > 15K€
- Coûts no-code > 1,000€/mois
- Feedback clients: features limitées no-code

### Sprint 4: Backend Foundation (Semaines 9-11)

#### Architecture Cible

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND                           │
│              Next.js 15 + React 19                   │
│        TypeScript + Tailwind CSS + shadcn/ui         │
└─────────────────────────────────────────────────────┘
                        │
                        │ REST/GraphQL
                        ▼
┌─────────────────────────────────────────────────────┐
│                BACKEND API LAYER                     │
│              Python FastAPI + Pydantic               │
│                   JWT Auth                           │
└─────────────────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│   Core     │  │  Workers   │  │   Cache    │
│  Services  │  │  (Celery)  │  │   (Redis)  │
└────────────┘  └────────────┘  └────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│              DATABASE (PostgreSQL)                   │
│         + Migrations (Alembic)                       │
└─────────────────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│  Bridge    │  │  Claude    │  │ SendGrid   │
│    API     │  │    API     │  │    API     │
└────────────┘  └────────────┘  └────────────┘
```

#### Stack Technique Final

**Backend**:
- **Framework**: FastAPI 0.110+
- **Language**: Python 3.12+
- **ORM**: SQLAlchemy 2.0+ (async)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Auth**: JWT (PyJWT) + OAuth2
- **Tasks**: Celery + Redis
- **Testing**: Pytest + Coverage (90%+)

**Frontend**:
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5.3+
- **UI**: Tailwind CSS + shadcn/ui
- **State**: Zustand / TanStack Query
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts / Chart.js
- **Testing**: Vitest + Testing Library

**Infrastructure**:
- **Database**: PostgreSQL 16 (Supabase or self-hosted)
- **Cache**: Redis 7
- **Queue**: Redis (Celery broker)
- **Storage**: S3-compatible (Supabase Storage)
- **Hosting**: Railway or Fly.io
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry + Posthog

#### Semaine 9-10: Backend API Core

**Objectifs**:
- ✅ Setup projet Python
- ✅ Database models (SQLAlchemy)
- ✅ API endpoints CRUD
- ✅ Authentication JWT

**Structure Projet**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── config.py                  # Settings (Pydantic)
│   ├── database.py                # DB session
│   │
│   ├── models/                    # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bank_account.py
│   │   ├── transaction.py
│   │   ├── invoice.py
│   │   ├── reconciliation.py
│   │   └── audit_log.py
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── bank_account.py
│   │   ├── transaction.py
│   │   └── invoice.py
│   │
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   ├── deps.py               # Dependencies (auth, db)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── bank_accounts.py
│   │   │   ├── transactions.py
│   │   │   ├── invoices.py
│   │   │   └── reconciliations.py
│   │
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── bank_service.py
│   │   ├── transaction_service.py
│   │   ├── reconciliation_service.py
│   │   ├── invoice_service.py
│   │   └── ai_service.py         # Claude integration
│   │
│   ├── workers/                   # Celery tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── bank_sync.py
│   │   ├── reconciliation.py
│   │   ├── reminders.py
│   │   └── forecasting.py
│   │
│   ├── integrations/              # External APIs
│   │   ├── __init__.py
│   │   ├── bridge.py
│   │   ├── claude.py
│   │   ├── sendgrid.py
│   │   └── pennylane.py
│   │
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── security.py
│       ├── validators.py
│       └── exceptions.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── alembic/                       # DB migrations
│   ├── versions/
│   └── env.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── pyproject.toml
└── README.md
```

#### Semaine 11: Workers & Background Jobs

**Objectifs**:
- ✅ Setup Celery + Redis
- ✅ Migrate workflows Make.com → Celery tasks
- ✅ Scheduler (Celery Beat)

**Celery Tasks**:
```python
# workers/bank_sync.py

@celery_app.task(bind=True, max_retries=3)
def sync_bank_transactions(self, bank_account_id: str):
    """
    Sync transactions from Bridge API for a bank account.
    Runs daily at 6:00 AM.
    """
    try:
        # Get bank account
        bank_account = BankAccountService.get(bank_account_id)
        
        # Fetch from Bridge API
        bridge_client = BridgeClient()
        transactions = bridge_client.get_transactions(
            account_id=bank_account.bridge_account_id,
            since=bank_account.last_sync_at
        )
        
        # Process each transaction
        for tx in transactions:
            # Check if exists
            existing = TransactionService.get_by_bridge_id(tx.id)
            if existing:
                continue
            
            # Categorize with AI
            category, confidence = AIService.categorize_transaction(
                description=tx.description,
                amount=tx.amount
            )
            
            # Create transaction
            TransactionService.create(
                bank_account_id=bank_account_id,
                bridge_transaction_id=tx.id,
                date=tx.date,
                description=tx.description,
                amount=tx.amount,
                category=category,
                category_confidence=confidence
            )
            
            # Trigger reconciliation check
            check_reconciliation.delay(transaction.id)
        
        # Update last_sync
        BankAccountService.update_last_sync(bank_account_id)
        
        return {"synced": len(transactions)}
        
    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
```

### Sprint 5-6: Frontend Migration (Semaines 12-16)

#### Semaine 12-14: Core UI Components
**Objectifs**:
- ✅ Setup Next.js project
- ✅ Design system (shadcn/ui)
- ✅ Core pages migration

**Structure Frontend**:
```
frontend/
├── src/
│   ├── app/                       # Next.js 15 App Router
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/
│   │   │   ├── page.tsx          # Dashboard
│   │   │   ├── transactions/
│   │   │   ├── invoices/
│   │   │   ├── reconciliations/
│   │   │   └── settings/
│   │   ├── layout.tsx
│   │   └── globals.css
│   │
│   ├── components/
│   │   ├── ui/                   # shadcn components
│   │   ├── dashboard/
│   │   ├── transactions/
│   │   ├── invoices/
│   │   ├── charts/
│   │   └── layout/
│   │
│   ├── lib/
│   │   ├── api.ts                # API client
│   │   ├── auth.ts
│   │   ├── utils.ts
│   │   └── validators.ts
│   │
│   ├── hooks/
│   │   ├── use-auth.ts
│   │   ├── use-transactions.ts
│   │   └── use-invoices.ts
│   │
│   ├── store/                    # Zustand
│   │   ├── auth.ts
│   │   └── ui.ts
│   │
│   └── types/
│       ├── api.ts
│       └── models.ts
│
├── public/
├── tests/
├── .env.local.example
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

#### Semaine 15-16: Advanced Features
**Objectifs**:
- ✅ Real-time updates (WebSockets)
- ✅ Optimistic UI updates
- ✅ Advanced charts
- ✅ Export features

### Sprint 7: Testing & Security (Semaines 17-18)

#### Semaine 17: Comprehensive Testing

**Backend Tests** (Target: 90%+ coverage):
```python
# tests/unit/services/test_reconciliation_service.py

def test_exact_match_reconciliation():
    """Test exact amount + date match."""
    transaction = create_test_transaction(
        amount=1500.00,
        date="2026-01-15",
        description="Paiement ACME Corp"
    )
    invoice = create_test_invoice(
        amount=1500.00,
        due_date="2026-01-12",
        client_name="ACME Corp"
    )
    
    match = ReconciliationService.find_match(transaction, invoice)
    
    assert match.score >= 0.95
    assert match.method == "exact"

def test_fuzzy_match_with_ai():
    """Test AI-based fuzzy matching."""
    transaction = create_test_transaction(
        amount=2450.50,
        description="VIR SEP A DUPONT JEAN REF:INV-2024-042"
    )
    invoice = create_test_invoice(
        invoice_number="INV-2024-042",
        amount=2450.50,
        client_name="Jean Dupont"
    )
    
    match = ReconciliationService.find_match(transaction, invoice)
    
    assert match.score >= 0.85
    assert match.method == "fuzzy_ai"
    assert "INV-2024-042" in match.reasoning

# tests/integration/test_bank_sync_flow.py

@pytest.mark.integration
async def test_complete_bank_sync_flow(db_session, mock_bridge_api):
    """Test complete flow: Bridge API → DB → Categorization → Reconciliation."""
    # Setup
    user = create_test_user()
    bank_account = create_test_bank_account(user_id=user.id)
    invoice = create_test_invoice(user_id=user.id, amount=1000.00)
    
    # Mock Bridge API response
    mock_bridge_api.return_value = [
        {
            "id": "bridge_tx_123",
            "date": "2026-01-20",
            "description": "Paiement client",
            "amount": 1000.00
        }
    ]
    
    # Execute sync
    result = await sync_bank_transactions(bank_account.id)
    
    # Assertions
    assert result["synced"] == 1
    
    # Check transaction created
    transaction = db_session.query(Transaction).filter_by(
        bridge_transaction_id="bridge_tx_123"
    ).first()
    assert transaction is not None
    assert transaction.category is not None
    assert transaction.category_confidence > 0.7
    
    # Check auto-reconciliation
    reconciliation = db_session.query(Reconciliation).filter_by(
        transaction_id=transaction.id
    ).first()
    assert reconciliation is not None
    assert reconciliation.invoice_id == invoice.id
```

**Frontend Tests**:
```typescript
// tests/components/TransactionsList.test.tsx

describe('TransactionsList', () => {
  it('should display transactions grouped by date', () => {
    const transactions = [
      { id: '1', date: '2026-01-20', amount: 1000, description: 'Test' },
      { id: '2', date: '2026-01-20', amount: -500, description: 'Test 2' },
    ];
    
    render(<TransactionsList transactions={transactions} />);
    
    expect(screen.getByText('20 janvier 2026')).toBeInTheDocument();
    expect(screen.getAllByRole('row')).toHaveLength(3); // Header + 2 rows
  });
  
  it('should show reconciliation status badge', () => {
    const transaction = {
      id: '1',
      is_reconciled: true,
      reconciliation: { match_score: 0.95 }
    };
    
    render(<TransactionRow transaction={transaction} />);
    
    expect(screen.getByText('Rapproché')).toBeInTheDocument();
    expect(screen.getByText('95%')).toBeInTheDocument();
  });
});
```

#### Semaine 18: Security Hardening

**Checklist Sécurité**:
- [ ] **Authentication**:
  - JWT avec refresh tokens
  - Rate limiting (10 req/min login)
  - Password hashing (bcrypt)
  - 2FA optional (TOTP)

- [ ] **Authorization**:
  - RBAC (Role-Based Access Control)
  - Row-level security (RLS) PostgreSQL
  - API endpoint permissions

- [ ] **Data Protection**:
  - Encryption at rest (database)
  - Encryption in transit (TLS 1.3)
  - PII data masking logs
  - GDPR compliance (data export/delete)

- [ ] **API Security**:
  - CORS configuration
  - CSRF protection
  - Input validation (Pydantic)
  - SQL injection prevention (ORM)
  - XSS prevention (sanitization)

- [ ] **External APIs**:
  - API keys in environment variables
  - OAuth2 flows (Bridge API)
  - Webhook signature verification
  - Rate limiting external calls

- [ ] **Monitoring**:
  - Sentry error tracking
  - Audit logs (all actions)
  - Failed login attempts tracking
  - Anomaly detection (unusual activity)

### Sprint 8: Deployment & Monitoring (Semaines 19-20)

#### Semaine 19: CI/CD Pipeline

**GitHub Actions Workflows**:

```yaml
# .github/workflows/backend-ci.yml

name: Backend CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linters
        run: |
          black --check .
          ruff check .
          mypy .
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test
          REDIS_URL: redis://localhost:6379/0
        run: |
          pytest --cov=app --cov-report=xml --cov-report=term
      
      - name: Check coverage
        run: |
          coverage report --fail-under=90
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Bandit (security)
        run: |
          pip install bandit
          bandit -r app/ -f json -o bandit-report.json
      
      - name: Run Safety (dependencies)
        run: |
          pip install safety
          safety check --json

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t financeai-backend:latest .
      
      - name: Push to registry
        run: |
          docker tag financeai-backend:latest registry.railway.app/financeai-backend:latest
          docker push registry.railway.app/financeai-backend:latest
```

#### Semaine 20: Production Deployment

**Infrastructure as Code** (Railway):
```yaml
# railway.toml

[build]
builder = "DOCKERFILE"
dockerfilePath = "./Dockerfile"

[deploy]
numReplicas = 2
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[[deploy.healthcheck]]
path = "/health"
port = 8000

[env]
DATABASE_URL = { type = "secret" }
REDIS_URL = { type = "secret" }
CLAUDE_API_KEY = { type = "secret" }
BRIDGE_API_KEY = { type = "secret" }
SENDGRID_API_KEY = { type = "secret" }
SECRET_KEY = { type = "secret" }
SENTRY_DSN = { type = "secret" }
```

**Monitoring Setup**:
- Sentry: Error tracking + performance
- Posthog: Product analytics
- Railway Metrics: CPU, memory, requests
- Uptime monitoring: UptimeRobot
- Log aggregation: Better Stack

---

## PHASE 3: SCALE & ENTERPRISE (MOIS 6-12)

### Features Avancées

**Q3 2026** (Mois 6-9):
- [ ] Multi-utilisateurs par entreprise (roles)
- [ ] API publique (webhooks, REST)
- [ ] Intégrations natives (Slack, Teams)
- [ ] Mobile app (React Native)
- [ ] White-label pour comptables
- [ ] Advanced reporting (BI)
- [ ] Prévisions ML (pas juste LLM)

**Q4 2026** (Mois 9-12):
- [ ] Multi-devises (EUR, USD, GBP)
- [ ] Multi-entités (holdings)
- [ ] Conformité avancée (export FEC, DAS2)
- [ ] Intégrations ERP enterprise (SAP, Oracle)
- [ ] AI copilot (chat assistant)
- [ ] Workflow automation builder (no-code interne)

---

## 📊 MILESTONES & KPIs

### Phase 1 Success Criteria (Semaine 8)
- ✅ MVP fonctionnel (5 features core)
- ✅ 20-30 clients beta payants
- ✅ NPS > 40
- ✅ Churn < 5%
- ✅ 90%+ précision réconciliations
- ✅ < 10 bugs critiques

### Phase 2 Success Criteria (Semaine 20)
- ✅ Migration 100% clients no-code → code
- ✅ 50-100 clients actifs
- ✅ API performance: p95 < 500ms
- ✅ Uptime > 99.5%
- ✅ Test coverage > 90%
- ✅ Zero security incidents

### Phase 3 Success Criteria (Mois 12)
- ✅ 200-500 clients
- ✅ 100K-250K€ MRR
- ✅ 2-3 intégrations majeures (Slack, SAP, etc.)
- ✅ Mobile app launched
- ✅ API publique 50+ utilisateurs
- ✅ Team 3-5 personnes

---

## 🔧 OUTILS & INFRASTRUCTURE

### Développement
- **IDE**: Cursor, VS Code
- **Version Control**: GitHub
- **Project Management**: Linear, Notion
- **Design**: Figma
- **API Testing**: Postman, HTTPie

### Production
- **Hosting**: Railway (backend + DB + Redis)
- **Frontend**: Vercel
- **CDN**: Cloudflare
- **Monitoring**: Sentry, Posthog
- **Logs**: Better Stack
- **Uptime**: UptimeRobot
- **Backups**: Automated daily (Railway)

### Communication
- **Email**: SendGrid
- **SMS** (optional): Twilio
- **Notifications**: Push (OneSignal)
- **Support**: Intercom or Crisp

---

## 💰 BUDGET PAR PHASE

### Phase 1 (No-Code MVP): 2,500€
- Validation: 500€
- No-code tools (2 mois): 400€
- APIs (Bridge, Claude, SendGrid): 300€
- Légal + domaines: 500€
- Design/branding: 400€
- Contingence: 400€

### Phase 2 (Migration Code): 3,500€
- Hosting (Railway): 500€
- Développement (si freelance partiel): 2,000€
- Migration data: 300€
- Testing & QA: 400€
- Contingence: 300€

### Phase 3 (Scale): Budget opérationnel (MRR)
- Infrastructure: 500-1,000€/mois
- APIs: 500-1,500€/mois
- Team (si embauche): 5,000-10,000€/mois
- Marketing: 2,000-5,000€/mois

---

## ⚠️ RISQUES & MITIGATION

| Risque | Impact | Mitigation |
|--------|--------|------------|
| **Migration complexe no-code → code** | Élevé | Migration progressive, double-run 2 semaines |
| **Performance dégradée** | Élevé | Load testing avant migration, caching agressif |
| **Bugs critiques production** | Élevé | Staging environment, feature flags, rollback plan |
| **Coûts infrastructure explosent** | Moyen | Alertes budgets, auto-scaling avec limites |
| **Perte données** | Critique | Backups automatiques quotidiens, disaster recovery plan |
| **Breach sécurité** | Critique | Penetration testing, security audits, insurance cyber |

---

## 📚 DOCUMENTATION

### À Créer
- [ ] README.md (setup instructions)
- [ ] API Documentation (OpenAPI/Swagger)
- [ ] Architecture Decision Records (ADR)
- [ ] Runbooks (incidents, deployments)
- [ ] User Documentation (guides, tutorials)
- [ ] Onboarding Dev (nouveau dev en 1 jour)

---

*Roadmap créée: Janvier 2026*
*Prochaine étape: Créer .cursorrules pour code quality*

