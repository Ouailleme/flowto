# 🤖 ROADMAP D'EXÉCUTION - IA DEVELOPER

## 🎯 CONTEXTE

**Développeur**: IA Claude (Anthropic)  
**Stack**: Python FastAPI + Next.js 15 + PostgreSQL + Redis  
**Design System**: DESIGN_SYSTEM_2026.md (le plus beau et pratique de 2026)  
**Objectif**: MVP production-ready en 2 semaines  
**Standards**: .cursorrules (Sécurité, Tests 90%+, Performance < 500ms)

---

## 📅 PLANNING (14 JOURS)

### SEMAINE 1: BACKEND (Jours 1-7)

#### JOUR 1: Foundation & Auth (8h)
**Priorité**: 🔴 CRITIQUE

**Tâches**:
1. **Setup projet backend** (1h)
   ```bash
   cd backend
   mkdir -p app/{models,schemas,api/v1,services,integrations,workers,core,utils}
   touch app/__init__.py
   # Créer tous les __init__.py
   ```

2. **Core utilities** (1h)
   - ✅ `app/config.py` - Déjà créé (international-ready)
   - ✅ `app/core/database.py` - Session async, Base
   - ✅ `app/core/security.py` - JWT, password hashing
   - ✅ `app/core/i18n.py` - Déjà créé
   - ✅ `app/core/currency.py` - Déjà créé

3. **Database models** (2h)
   - ✅ `app/models/user.py` - Déjà créé (international-ready)
   - ✅ `app/models/transaction.py` - Déjà créé (multi-currency)
   - `app/models/bank_account.py`
   - `app/models/invoice.py`
   - `app/models/reconciliation.py`
   - `app/models/reminder.py`
   - `app/models/audit_log.py`

4. **Pydantic schemas** (1h)
   - `app/schemas/user.py` (UserCreate, UserRead, UserUpdate)
   - `app/schemas/auth.py` (Token, TokenData)

5. **Auth system** (2h)
   - `app/api/deps.py` (get_current_user, get_db)
   - `app/services/auth_service.py` (register, login, verify)
   - `app/api/v1/auth.py` (POST /register, POST /login, GET /me)

6. **Main app** (30min)
   - `app/main.py` (FastAPI app, CORS, routers)

7. **Tests auth** (30min)
   - `tests/conftest.py` (fixtures)
   - `tests/unit/test_auth_service.py`
   - `tests/integration/test_auth_api.py`

**Validation**:
```bash
pytest --cov=app/services/auth_service --cov=app/api/v1/auth
# Coverage > 90% ✅
curl -X POST http://localhost:8000/api/v1/auth/register
curl -X POST http://localhost:8000/api/v1/auth/login
# → JWT token ✅
```

---

#### JOUR 2: Core Models & CRUD (8h)

**Tâches**:
1. **Compléter models** (2h)
   - `app/models/bank_account.py`
   - `app/models/invoice.py`
   - `app/models/reconciliation.py`
   - `app/models/reminder.py`
   - `app/models/audit_log.py`
   - Relationships entre models

2. **Pydantic schemas** (2h)
   - `app/schemas/bank.py`
   - `app/schemas/transaction.py`
   - `app/schemas/invoice.py`
   - `app/schemas/reconciliation.py`

3. **Services CRUD** (3h)
   - `app/services/bank_service.py`
   - `app/services/transaction_service.py`
   - `app/services/invoice_service.py`
   - Pagination, filtres, tri

4. **API Routes** (1h)
   - `app/api/v1/banks.py` (CRUD complet)
   - `app/api/v1/transactions.py` (GET list + filters)
   - `app/api/v1/invoices.py` (CRUD complet)

**Validation**:
```bash
# Postman collection: 15+ endpoints testés
# Tous les CRUD fonctionnent ✅
```

---

#### JOUR 3: External Integrations (8h)

**Tâches**:
1. **Bridge API Client** (3h)
   - `app/integrations/bridge_client.py`
   - Methods:
     * `generate_connect_url()` - Connexion banque
     * `get_accounts()` - Liste comptes
     * `get_transactions()` - Transactions
   - Retry logic (tenacity)
   - Error handling
   - Tests avec mocks

2. **Claude AI Client** (2h)
   - `app/integrations/claude_client.py`
   - Methods:
     * `categorize_transaction()` - Catégorisation
     * `match_transaction_invoice()` - Fuzzy matching
     * `generate_reminder_email()` - Génération email
   - Gestion tokens (anthropic library)
   - Caching responses

3. **SendGrid Client** (1h)
   - `app/integrations/sendgrid_client.py`
   - Methods:
     * `send_reminder()`
     * `send_welcome_email()`
   - Templates multilingues

4. **Integration dans API** (1h)
   - `app/api/v1/banks.py` → POST /connect
   - Workflow: Generate URL → User connects → Webhook callback

5. **Tests intégration** (1h)
   - Mocks pour APIs externes
   - Tests E2E simulés

**Validation**:
```bash
pytest tests/integration/test_bridge_client.py
pytest tests/integration/test_claude_client.py
# Tous les tests passent ✅
```

---

#### JOUR 4: Celery Workers (8h)

**Tâches**:
1. **Setup Celery** (1h)
   - `app/workers/celery_app.py`
   - Configuration (broker Redis, backend)
   - Schedules (beat)

2. **Bank Sync Worker** (3h)
   - `app/workers/bank_sync.py`
   - Task: `sync_bank_transactions(bank_account_id)`
   - Flow:
     1. Get transactions from Bridge
     2. Categorize with Claude
     3. Save to DB
     4. Trigger reconciliation
   - Retry logic
   - Error handling

3. **Reconciliation Worker** (2h)
   - `app/workers/reconciliation.py`
   - Task: `auto_reconcile_transaction(transaction_id)`
   - Flow:
     1. Exact match (amount + date ±3 days)
     2. If not found → Fuzzy match (Claude)
     3. If confidence > 0.8 → Auto-validate
     4. Else → Manual review

4. **Reminders Worker** (1h)
   - `app/workers/reminders.py`
   - Task: `send_payment_reminders()`
   - Cron: Daily 9 AM
   - Flow:
     1. Get overdue invoices
     2. Generate email (Claude)
     3. Send (SendGrid)
     4. Log in DB

5. **Tests workers** (1h)
   - Tests avec Celery test mode
   - Mocks pour APIs

**Validation**:
```bash
# Terminal 1: Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# Terminal 2: Trigger task
python -c "from app.workers.bank_sync import sync_bank_transactions; sync_bank_transactions.delay('bank-id')"
# → Task exécutée ✅
```

---

#### JOUR 5: Tests & Documentation (8h)

**Tâches**:
1. **Unit tests** (3h)
   - `tests/unit/test_auth_service.py`
   - `tests/unit/test_bank_service.py`
   - `tests/unit/test_transaction_service.py`
   - `tests/unit/test_invoice_service.py`
   - Coverage > 90% obligatoire

2. **Integration tests** (2h)
   - `tests/integration/test_api.py`
   - Test tous les endpoints
   - Test auth flow
   - Test CRUD complet

3. **E2E tests** (2h)
   - `tests/e2e/test_full_flow.py`
   - Scenario: Signup → Connect bank → Sync → Create invoice → Reconcile

4. **Documentation API** (1h)
   - Swagger auto-généré (FastAPI)
   - Ajouter descriptions
   - Ajouter exemples

**Validation**:
```bash
pytest --cov=app --cov-report=html
# Coverage: 92% ✅
open htmlcov/index.html
```

---

#### JOUR 6-7: Polish Backend (16h)

**Tâches**:
1. **Optimizations** (4h)
   - Indexes database
   - Caching (Redis)
   - Query optimization
   - N+1 queries fix

2. **Security hardening** (4h)
   - Rate limiting (slowapi)
   - Input validation stricte
   - SQL injection prevention (déjà OK avec ORM)
   - XSS prevention
   - CSRF tokens

3. **Monitoring** (2h)
   - Structured logging (structlog)
   - Sentry integration
   - Metrics (Prometheus-ready)

4. **Alembic migrations** (2h)
   - Init Alembic
   - Create initial migration
   - Test upgrade/downgrade

5. **Docker** (2h)
   - Dockerfile backend optimisé
   - docker-compose.yml complet
   - Health checks

6. **CI/CD** (2h)
   - GitHub Actions
   - Tests auto
   - Linting (black, ruff, mypy)

**Validation**:
```bash
# Backend complet et testé ✅
# Prêt pour production ✅
```

---

### SEMAINE 2: FRONTEND (Jours 8-14)

#### JOUR 8: Setup & Design System (8h)

**Tâches**:
1. **Init Next.js** (1h)
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --app
   cd frontend
   npm install @tanstack/react-query axios zustand react-hook-form zod
   npm install framer-motion lucide-react date-fns
   npx shadcn-ui@latest init
   ```

2. **Install shadcn components** (1h)
   ```bash
   npx shadcn-ui@latest add button card input label
   npx shadcn-ui@latest add dropdown-menu avatar badge
   npx shadcn-ui@latest add table dialog toast
   npx shadcn-ui@latest add select checkbox textarea
   ```

3. **Theme setup** (2h)
   - `src/app/globals.css` - Variables CSS (DESIGN_SYSTEM_2026.md)
   - `src/components/theme-provider.tsx` - Dark mode
   - `src/components/theme-toggle.tsx` - Toggle button

4. **API client** (2h)
   - `src/lib/api-client.ts` - Axios wrapper
   - Request interceptor (JWT)
   - Response interceptor (errors)
   - Types TypeScript

5. **Layout base** (2h)
   - `src/app/layout.tsx` - Root layout
   - `src/components/layout/header.tsx`
   - `src/components/layout/sidebar.tsx`
   - `src/components/layout/footer.tsx`

**Validation**:
```bash
npm run dev
# App se lance ✅
# Dark mode fonctionne ✅
```

---

#### JOUR 9: Auth Pages (8h)

**Tâches**:
1. **Auth layouts** (1h)
   - `src/app/(auth)/layout.tsx` - Layout auth (centered)

2. **Login page** (2h)
   - `src/app/(auth)/login/page.tsx`
   - Form (React Hook Form + Zod)
   - API call `/api/v1/auth/login`
   - Store token (localStorage)
   - Redirect to dashboard

3. **Signup page** (2h)
   - `src/app/(auth)/signup/page.tsx`
   - Multi-step form:
     * Step 1: Email, Password
     * Step 2: Company info
     * Step 3: Preferences (language, currency)
   - API call `/api/v1/auth/register`
   - Auto-login après signup

4. **Auth hooks** (2h)
   - `src/hooks/use-auth.ts` - useAuth hook
   - `src/store/auth-store.ts` - Zustand store
   - Protected routes HOC

5. **Tests** (1h)
   - Vitest + Testing Library
   - Test login flow
   - Test signup flow

**Validation**:
```bash
# Signup → Login → Dashboard ✅
# Token stocké ✅
# Protected routes ✅
```

---

#### JOUR 10: Dashboard (8h)

**Tâches**:
1. **Dashboard layout** (1h)
   - `src/app/(dashboard)/layout.tsx`
   - Sidebar navigation
   - Header with user menu

2. **Dashboard page** (3h)
   - `src/app/(dashboard)/page.tsx`
   - 4 KPI cards:
     * Solde total
     * Factures en attente
     * Trésorerie prévue (30j)
     * Rapprochements à valider
   - Chart: Évolution trésorerie (Recharts)
   - Recent transactions (5 dernières)

3. **Data fetching** (2h)
   - `src/hooks/use-dashboard.ts` - TanStack Query
   - API calls pour KPIs
   - Polling pour données live

4. **Micro-interactions** (1h)
   - Hover effects (Framer Motion)
   - Loading skeletons
   - Fade in animations

5. **Tests** (1h)
   - Test KPIs display
   - Test chart rendering

**Validation**:
```bash
# Dashboard affiche vraies données ✅
# Charts animés ✅
# Performance < 2s load ✅
```

---

#### JOUR 11: Banks & Transactions (8h)

**Tâches**:
1. **Banks page** (3h)
   - `src/app/(dashboard)/banks/page.tsx`
   - Liste comptes bancaires (cards)
   - Button "Connecter une banque"
   - Modal Bridge connect URL
   - Sync button par compte
   - Last sync timestamp

2. **Transactions page** (4h)
   - `src/app/(dashboard)/transactions/page.tsx`
   - Data table (shadcn)
   - Filtres:
     * Date range picker
     * Category select
     * Amount range
     * Reconciled yes/no
   - Sorting
   - Pagination (server-side)
   - Export CSV button

3. **Hooks** (1h)
   - `src/hooks/use-banks.ts`
   - `src/hooks/use-transactions.ts`
   - TanStack Query avec filters

**Validation**:
```bash
# Connect bank modal ✅
# Transactions list avec filtres ✅
# Performance table 10k+ rows ✅
```

---

#### JOUR 12: Invoices & Reconciliations (8h)

**Tâches**:
1. **Invoices page** (4h)
   - `src/app/(dashboard)/invoices/page.tsx`
   - Liste factures (cards ou table)
   - Button "Nouvelle facture"
   - Form modal:
     * Client name
     * Amount
     * Due date
     * Notes
   - Status badges (pending, paid, overdue)
   - Actions: Edit, Delete, Send reminder

2. **Reconciliations page** (3h)
   - `src/app/(dashboard)/reconciliations/page.tsx`
   - Pending reconciliations
   - Pour chaque:
     * Transaction card
     * Invoice card
     * Match score (progress bar)
     * Buttons: Validate, Reject
   - Filters: Score > 0.8, Date range

3. **Hooks** (1h)
   - `src/hooks/use-invoices.ts`
   - `src/hooks/use-reconciliations.ts`

**Validation**:
```bash
# Create invoice ✅
# View reconciliation suggestions ✅
# Validate reconciliation ✅
```

---

#### JOUR 13: Settings & Polish (8h)

**Tâches**:
1. **Settings page** (4h)
   - `src/app/(dashboard)/settings/page.tsx`
   - Tabs:
     * Account (email, company, language, currency)
     * Preferences (timezone, dark mode)
     * Subscription (plan, billing)
     * Security (password change, 2FA future)
   - Forms avec validation

2. **UI Polish** (2h)
   - Micro-interactions partout
   - Loading states cohérents
   - Error boundaries
   - Toast notifications
   - Empty states (illustrations)

3. **Mobile responsive** (1h)
   - Test sur mobile
   - Adjust layouts
   - Touch-friendly buttons

4. **Accessibility** (1h)
   - Keyboard navigation
   - ARIA labels
   - Screen reader test
   - Contrast check

**Validation**:
```bash
# Settings fonctionnent ✅
# Mobile responsive ✅
# Accessibility score > 90 (Lighthouse) ✅
```

---

#### JOUR 14: Tests & Deploy (8h)

**Tâches**:
1. **E2E tests** (4h)
   - Playwright setup
   - Test: Complete user journey
     * Signup
     * Connect bank
     * View transactions
     * Create invoice
     * Validate reconciliation

2. **Performance** (2h)
   - Lighthouse audit
   - Optimize images (Next.js Image)
   - Code splitting
   - Bundle analysis

3. **Deploy** (2h)
   - Backend: Railway
   - Frontend: Vercel
   - Database: Supabase
   - Redis: Railway
   - Env variables
   - Health checks

**Validation**:
```bash
# E2E tests passent ✅
# Lighthouse score > 90 ✅
# App deployée et accessible ✅
```

---

## ✅ DELIVRABLES FIN SEMAINE 2

### Backend ✅
- [x] 30+ endpoints API documentés
- [x] Tests coverage > 90%
- [x] 4 workers Celery fonctionnels
- [x] 3 intégrations externes (Bridge, Claude, SendGrid)
- [x] Sécurité: JWT, RBAC, audit logs
- [x] Performance: < 200ms p95
- [x] Docker + CI/CD

### Frontend ✅
- [x] 10 pages complètes
- [x] Design system implémenté (DESIGN_SYSTEM_2026.md)
- [x] Responsive mobile/tablet/desktop
- [x] Dark mode
- [x] Accessibility WCAG 2.2
- [x] Tests E2E
- [x] Performance Lighthouse > 90

### International-Ready ✅
- [x] Multi-langues (FR, EN, ES, DE, IT, NL)
- [x] Multi-devises (EUR, USD, GBP, CHF, CAD)
- [x] Multi-pays (11 pays via Bridge API)
- [x] Formats dates/nombres selon locale

---

## 🎯 MÉTRIQUES SUCCÈS

| Métrique | Target | Résultat |
|----------|--------|----------|
| **Backend Tests Coverage** | 90%+ | % |
| **Frontend Tests Coverage** | 80%+ | % |
| **API Response Time (p95)** | < 500ms | ms |
| **Page Load Time (LCP)** | < 2.5s | s |
| **Lighthouse Score** | > 90 | /100 |
| **Accessibility Score** | > 90 | /100 |
| **Bundle Size** | < 200KB | KB |
| **Number of Endpoints** | 30+ | endpoints |
| **Number of Components** | 50+ | components |

---

## 📋 DAILY CHECKLIST

Chaque jour:
- [ ] Code review (self)
- [ ] Tests (coverage > 90%)
- [ ] Lint (black, ruff, mypy, eslint)
- [ ] Git commit (conventional commits)
- [ ] Documentation update
- [ ] Performance check

---

## 🚀 POST-MVP (Semaines 3-4)

### Beta Test
- [ ] 5 early adopters
- [ ] Feedback collection
- [ ] Bug fixes
- [ ] UX improvements

### Features V1.1
- [ ] Cash flow forecasting
- [ ] Bulk operations
- [ ] Advanced filters
- [ ] Export accounting formats
- [ ] Mobile app (React Native)

---

**JE SUIS PRÊT À DÉVELOPPER ! 🔥**

**NEXT**: Commencer JOUR 1 → `backend/app/core/database.py`


