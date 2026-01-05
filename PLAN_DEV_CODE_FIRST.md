# 🔥 PLAN DÉVELOPPEMENT CODE-FIRST - FinanceAI

## 🎯 STACK TECHNIQUE 2026 (Best-in-Class)

### Backend
- **Framework**: Python 3.12 + FastAPI (async/await)
- **Database**: PostgreSQL 16 + SQLAlchemy (async)
- **Cache**: Redis 7
- **Queue**: Celery + Redis
- **IA**: LangGraph + Claude 3.5 Sonnet / GPT-4o mini
- **APIs**: Bridge API (banques), SendGrid (emails)

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript strict
- **UI**: shadcn/ui + Tailwind CSS
- **State**: TanStack Query + Zustand
- **Forms**: React Hook Form + Zod

### DevOps
- **Containerization**: Docker + Docker Compose
- **Deployment**: Railway / Fly.io
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry (errors) + Structured logging

### Database
- **Primary**: PostgreSQL (Supabase)
- **Migrations**: Alembic
- **ORM**: SQLAlchemy 2.0 (async)

---

## 📁 STRUCTURE PROJET

```
financeai/
├── backend/                    # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Settings (pydantic-settings)
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── bank_account.py
│   │   │   ├── transaction.py
│   │   │   ├── invoice.py
│   │   │   └── reconciliation.py
│   │   ├── schemas/           # Pydantic schemas (API)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── bank.py
│   │   │   ├── transaction.py
│   │   │   └── invoice.py
│   │   ├── api/               # API routes
│   │   │   ├── __init__.py
│   │   │   ├── deps.py        # Dependencies (auth, db)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── banks.py
│   │   │       ├── transactions.py
│   │   │       ├── invoices.py
│   │   │       └── reconciliations.py
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── bank_service.py
│   │   │   ├── transaction_service.py
│   │   │   ├── invoice_service.py
│   │   │   └── reconciliation_service.py
│   │   ├── integrations/      # External APIs
│   │   │   ├── __init__.py
│   │   │   ├── bridge_client.py
│   │   │   ├── claude_client.py
│   │   │   └── sendgrid_client.py
│   │   ├── workers/           # Celery tasks
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   ├── bank_sync.py
│   │   │   ├── reconciliation.py
│   │   │   └── reminders.py
│   │   ├── core/              # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py    # JWT, password hashing
│   │   │   ├── database.py    # DB session
│   │   │   └── logging.py     # Structured logging
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py        # Pytest fixtures
│   │   ├── unit/
│   │   │   ├── test_services.py
│   │   │   └── test_models.py
│   │   ├── integration/
│   │   │   └── test_api.py
│   │   └── e2e/
│   │       └── test_flows.py
│   ├── alembic/               # DB migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── requirements.txt       # Dependencies
│   ├── requirements-dev.txt   # Dev dependencies
│   ├── pyproject.toml         # Black, Ruff, mypy config
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # Next.js 15
│   ├── src/
│   │   ├── app/               # App Router
│   │   │   ├── (auth)/        # Auth layout group
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── signup/
│   │   │   │       └── page.tsx
│   │   │   ├── (dashboard)/   # Dashboard layout
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx   # Dashboard home
│   │   │   │   ├── banks/
│   │   │   │   ├── transactions/
│   │   │   │   ├── invoices/
│   │   │   │   ├── reconciliations/
│   │   │   │   └── settings/
│   │   │   ├── api/           # API routes (if needed)
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx       # Landing page
│   │   ├── components/
│   │   │   ├── ui/            # shadcn components
│   │   │   ├── layout/        # Layout components
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Footer.tsx
│   │   │   └── features/      # Feature components
│   │   │       ├── auth/
│   │   │       ├── banks/
│   │   │       ├── transactions/
│   │   │       └── invoices/
│   │   ├── lib/
│   │   │   ├── api-client.ts  # Axios wrapper
│   │   │   ├── auth.ts        # Auth helpers
│   │   │   └── utils.ts       # Utilities
│   │   ├── hooks/             # Custom hooks
│   │   │   ├── use-auth.ts
│   │   │   ├── use-banks.ts
│   │   │   └── use-transactions.ts
│   │   ├── store/             # Zustand stores
│   │   │   └── auth-store.ts
│   │   └── types/             # TypeScript types
│   │       ├── api.ts
│   │       ├── models.ts
│   │       └── index.ts
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── Dockerfile
│   └── .env.local.example
│
├── docker-compose.yml          # Dev environment
├── docker-compose.prod.yml     # Production
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── frontend-ci.yml
├── .gitignore
├── README.md
└── docs/
    ├── API.md                  # API documentation
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

---

## 🚀 PLAN DÉVELOPPEMENT (2 SEMAINES)

### SEMAINE 1: BACKEND + INFRASTRUCTURE

#### JOUR 1: Setup & Auth (6-8h)

**1. Init projet (1h)**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy asyncpg alembic pydantic-settings python-jose passlib bcrypt python-multipart redis celery
pip freeze > requirements.txt

# Frontend
cd ../frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
npm install @tanstack/react-query axios zustand react-hook-form zod @hookform/resolvers
npm install -D @types/node @types/react
npx shadcn-ui@latest init
```

**2. Database setup (1h)**
```bash
# Supabase project (ou local PostgreSQL)
# Copier database_schema.sql → SQL Editor → Run
# Récupérer connection string

# Backend: Alembic init
cd backend
alembic init alembic
# Configurer alembic.ini avec DATABASE_URL
```

**3. FastAPI base structure (2h)**
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FinanceAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

**4. Auth système complet (3-4h)**
```python
# models/user.py (SQLAlchemy model)
# schemas/user.py (Pydantic schemas)
# services/auth_service.py (Business logic)
# api/v1/auth.py (Endpoints: /register, /login, /me)
# core/security.py (JWT, password hashing)

# Endpoints à créer:
# POST /api/v1/auth/register
# POST /api/v1/auth/login
# GET /api/v1/auth/me
```

**Validation Jour 1**:
```bash
# Tester avec curl:
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!","company_name":"Test Corp"}'

curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}'
# → Retourne: {"access_token": "...", "token_type": "bearer"}
```

---

#### JOUR 2: Models & CRUD de base (6-8h)

**1. SQLAlchemy models (2h)**
```python
# models/bank_account.py
# models/transaction.py
# models/invoice.py
# models/reconciliation.py
# models/reminder.py
# models/audit_log.py

# Tous avec:
# - UUIDs as primary keys
# - created_at, updated_at timestamps
# - Soft delete (deleted_at)
# - Proper indexes
# - Foreign keys avec ondelete
```

**2. Pydantic schemas (1h)**
```python
# schemas/bank.py (BankAccountCreate, BankAccountRead, BankAccountUpdate)
# schemas/transaction.py
# schemas/invoice.py
# schemas/reconciliation.py

# Avec validations:
# - field_validator pour business rules
# - ConfigDict(from_attributes=True) pour ORM
# - Proper types (Decimal, datetime, UUID)
```

**3. CRUD services (2h)**
```python
# services/bank_service.py
# services/transaction_service.py
# services/invoice_service.py

# Méthodes:
# - create()
# - get_by_id()
# - get_multi() (avec pagination)
# - update()
# - delete() (soft delete)
```

**4. API endpoints (2h)**
```python
# api/v1/banks.py
# GET /api/v1/banks (list user's banks)
# POST /api/v1/banks (connect new bank)
# GET /api/v1/banks/{id}
# DELETE /api/v1/banks/{id}

# api/v1/transactions.py
# GET /api/v1/transactions (with filters)
# GET /api/v1/transactions/{id}

# api/v1/invoices.py
# GET /api/v1/invoices
# POST /api/v1/invoices
# GET /api/v1/invoices/{id}
# PATCH /api/v1/invoices/{id}
# DELETE /api/v1/invoices/{id}
```

**Validation Jour 2**:
```bash
# Postman/Insomnia collection avec 15+ requests
# Tous les endpoints testés manuellement
# Authorization header: Bearer <token>
```

---

#### JOUR 3: Intégrations externes (6-8h)

**1. Bridge API Client (3h)**
```python
# integrations/bridge_client.py

class BridgeClient:
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient(...)
    
    async def generate_connect_url(self, user_id: str) -> dict:
        """Generate URL for bank connection"""
    
    async def get_accounts(self, user_uuid: str) -> list[dict]:
        """Get user's bank accounts"""
    
    async def get_transactions(
        self,
        account_id: str,
        since: datetime
    ) -> list[dict]:
        """Fetch transactions"""
    
    # Avec retry logic (tenacity)
    # Avec timeouts
    # Avec error handling
```

**2. Claude AI Client (2h)**
```python
# integrations/claude_client.py

class ClaudeClient:
    async def categorize_transaction(
        self,
        description: str,
        amount: float
    ) -> dict:
        """Categorize transaction with AI
        Returns: {category: str, confidence: float}
        """
    
    async def match_transaction_invoice(
        self,
        transaction: dict,
        invoice: dict
    ) -> dict:
        """Fuzzy match transaction to invoice
        Returns: {match: bool, confidence: float, reasoning: str}
        """
    
    async def generate_reminder_email(
        self,
        invoice: dict,
        reminder_type: str
    ) -> dict:
        """Generate reminder email
        Returns: {subject: str, body: str}
        """
```

**3. SendGrid Client (1h)**
```python
# integrations/sendgrid_client.py

class SendGridClient:
    async def send_reminder(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> dict:
        """Send reminder email"""
```

**4. Integration dans API (1h)**
```python
# api/v1/banks.py
@router.post("/connect")
async def connect_bank(current_user: User = Depends(get_current_user)):
    bridge_client = BridgeClient(settings.BRIDGE_API_KEY)
    result = await bridge_client.generate_connect_url(str(current_user.id))
    return result
```

**Validation Jour 3**:
```bash
# Test chaque client individuellement
pytest tests/integration/test_bridge_client.py
pytest tests/integration/test_claude_client.py
pytest tests/integration/test_sendgrid_client.py
```

---

#### JOUR 4: Celery Workers (6-8h)

**1. Celery setup (1h)**
```python
# workers/celery_app.py
from celery import Celery

celery_app = Celery(
    "financeai",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Paris",
    enable_utc=True,
)
```

**2. Bank sync task (2h)**
```python
# workers/bank_sync.py

@celery_app.task(bind=True, max_retries=3)
def sync_bank_transactions(self, bank_account_id: str):
    """
    Sync transactions from Bridge API
    - Fetch new transactions
    - Categorize with Claude
    - Save to database
    - Trigger reconciliation
    """
    try:
        # Implementation
        pass
    except Exception as e:
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
```

**3. Auto-reconciliation task (2h)**
```python
# workers/reconciliation.py

@celery_app.task
def auto_reconcile_transaction(transaction_id: str):
    """
    Try to match transaction with invoices
    1. Exact match (amount + date)
    2. Fuzzy match with Claude AI
    3. Create reconciliation if confidence > 0.8
    """
    pass
```

**4. Reminders task (2h)**
```python
# workers/reminders.py

@celery_app.task
def send_payment_reminders():
    """
    Daily task to send reminders for overdue invoices
    - Find overdue invoices
    - Generate email with Claude
    - Send with SendGrid
    - Log in reminders table
    """
    pass
```

**Validation Jour 4**:
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# Terminal 3: Test tasks
python
>>> from app.workers.bank_sync import sync_bank_transactions
>>> sync_bank_transactions.delay("bank-uuid")
```

---

#### JOUR 5: Tests Backend (6-8h)

**1. Setup pytest (1h)**
```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app
from app.core.database import get_db

@pytest.fixture
async def db_session():
    # Create test database
    # Yield session
    # Cleanup
    pass

@pytest.fixture
async def test_user(db_session):
    # Create test user
    pass

@pytest.fixture
async def auth_headers(test_user):
    # Generate JWT token
    pass
```

**2. Unit tests (2h)**
```python
# tests/unit/test_auth_service.py
async def test_create_user_success():
    pass

async def test_login_invalid_credentials():
    pass

# tests/unit/test_transaction_service.py
async def test_categorize_transaction():
    pass
```

**3. Integration tests (2h)**
```python
# tests/integration/test_api.py
async def test_register_login_flow():
    pass

async def test_create_invoice():
    pass

async def test_bank_connection_flow():
    pass
```

**4. E2E tests (1h)**
```python
# tests/e2e/test_full_flow.py
async def test_complete_reconciliation_flow():
    """
    1. Create user
    2. Connect bank
    3. Sync transactions
    4. Create invoice
    5. Auto-reconciliation
    6. Verify invoice marked as paid
    """
    pass
```

**Validation Jour 5**:
```bash
pytest --cov=app --cov-report=html
# Target: 90%+ coverage
```

---

### SEMAINE 2: FRONTEND + INTEGRATION

#### JOUR 6-7: Frontend Base (12-16h)

**Structure composants**:
```typescript
// components/layout/Sidebar.tsx
// components/layout/Header.tsx
// components/features/auth/LoginForm.tsx
// components/features/auth/SignupForm.tsx
// components/features/banks/BankList.tsx
// components/features/banks/ConnectBankModal.tsx
// components/features/transactions/TransactionList.tsx
// components/features/transactions/TransactionFilters.tsx
// components/features/invoices/InvoiceForm.tsx
// components/features/invoices/InvoiceList.tsx
// components/features/reconciliations/ReconciliationCard.tsx
```

**API client setup**:
```typescript
// lib/api-client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 30000,
});

// Request interceptor: Add JWT
apiClient.interceptors.request.use(async (config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**TanStack Query hooks**:
```typescript
// hooks/use-banks.ts
export function useBanks() {
  return useQuery({
    queryKey: ['banks'],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/v1/banks');
      return data;
    },
  });
}

// hooks/use-transactions.ts
// hooks/use-invoices.ts
// etc.
```

---

#### JOUR 8-9: UI/UX Polish (12-16h)

- Dashboard avec KPIs
- Listes avec pagination
- Filtres avancés
- Loading states
- Error boundaries
- Toast notifications
- Mobile responsive

---

#### JOUR 10: Tests E2E Frontend (6-8h)

```typescript
// Playwright ou Cypress
test('complete user flow', async ({ page }) => {
  // 1. Signup
  await page.goto('/signup');
  await page.fill('[name="email"]', 'test@test.com');
  await page.fill('[name="password"]', 'Test123!');
  await page.click('button[type="submit"]');
  
  // 2. Login
  await page.waitForURL('/dashboard');
  
  // 3. Connect bank
  // 4. Verify transactions
});
```

---

## 🎯 MÉTRIQUES SUCCÈS FIN 2 SEMAINES

- [ ] Backend: 30+ endpoints fonctionnels
- [ ] Frontend: 10+ pages complètes
- [ ] Tests: 90%+ coverage backend, 80%+ frontend
- [ ] CI/CD: GitHub Actions configuré
- [ ] Docker: docker-compose up = app complète
- [ ] Documentation: API docs complète
- [ ] Performance: < 200ms response time p95
- [ ] Security: JWT, CORS, input validation, audit logs

---

## 💰 BUDGET

**Infrastructure (mensuel)**:
- Supabase: 25€/mois (Pro)
- Railway: 20€/mois (Hobby)
- Redis Cloud: 0€ (free tier 30MB)
- Sentry: 0€ (free tier 5k events/mois)
**Total**: 45€/mois

**APIs (variable)**:
- Bridge API: 0€ (sandbox), puis 0.01€/transaction
- Claude API: ~50€/mois (10k transactions/mois)
- SendGrid: 0€ (100 emails/jour free)
**Total**: ~50€/mois

**TOTAL MOIS 1**: ~95€

---

## 🚀 APRÈS 2 SEMAINES

Tu auras:
- ✅ App full-stack production-ready
- ✅ Code qualité (tests, linting, type-safe)
- ✅ Scalable (async, queue, cache)
- ✅ Sécurisée (JWT, RBAC, audit logs)
- ✅ Déployable en 1 commande
- ✅ Documentée (API, architecture)

**NEXT**:
- Beta test avec 5 early adopters
- Monitoring & alerting
- Performance optimization
- Features avancées (exports, analytics)

---

**ON Y VA! 🔥 Les meilleurs devs de 2026 = meilleur produit de 2026!**


