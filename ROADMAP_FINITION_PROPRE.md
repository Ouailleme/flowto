# 🎯 ROADMAP : Finition Propre du Projet FinanceAI

**Date de début** : 5 janvier 2026 - 23:30  
**Durée estimée** : 3-4 jours (20-22h)  
**Objectif** : Atteindre les standards professionnels du `.cursorrules`

---

## 📋 CHECKLIST GLOBALE

### Phase 1 : Tests Backend (Jour 1 - 6h)
- [ ] Configuration pytest avancée
- [ ] Tests unitaires services (90%+ couverture)
- [ ] Tests unitaires utils/security
- [ ] Tests d'intégration API
- [ ] Tests d'intégration DB
- [ ] Fixtures et factories
- [ ] Mocks pour API externes

### Phase 2 : Tests Frontend (Jour 1 - 2h)
- [ ] Configuration Vitest avancée
- [ ] Tests unitaires composants
- [ ] Tests unitaires hooks
- [ ] Tests formulaires + validation

### Phase 3 : Qualité & Linters (Jour 2 - 2h)
- [ ] Configurer pre-commit hooks
- [ ] Exécuter Black + Ruff + mypy
- [ ] Exécuter ESLint + Prettier
- [ ] Fixer toutes les erreurs linter
- [ ] Ajouter docstrings manquantes

### Phase 4 : Data & Workers (Jour 2 - 3h)
- [ ] Script seed data (users, invoices, transactions)
- [ ] Configuration Redis
- [ ] Configuration Celery workers
- [ ] Tests workers Celery
- [ ] Background jobs fonctionnels

### Phase 5 : Monitoring & Logs (Jour 2 - 2h)
- [ ] Configurer Sentry
- [ ] Logging structuré (structlog)
- [ ] Request ID tracking
- [ ] Error tracking backend
- [ ] Error tracking frontend

### Phase 6 : CI/CD (Jour 3 - 3h)
- [ ] GitHub Actions workflow
- [ ] Tests automatiques sur PR
- [ ] Linters automatiques
- [ ] Build Docker images
- [ ] Deploy preview (optionnel)

### Phase 7 : Documentation (Jour 3 - 2h)
- [ ] Consolider README.md
- [ ] Créer SETUP.md
- [ ] Créer ARCHITECTURE.md
- [ ] Créer CONTRIBUTING.md
- [ ] Supprimer docs obsolètes

### Phase 8 : Optimisations (Jour 4 - 2h)
- [ ] Ajouter indexes DB manquants
- [ ] Optimiser queries N+1
- [ ] Code splitting frontend
- [ ] Performance audit
- [ ] Sécurité audit

### Phase 9 : Déploiement (Jour 4 - 2h)
- [ ] Choisir plateforme (Railway, Render, AWS)
- [ ] Configuration production
- [ ] Variables d'environnement
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Tests smoke production

### Phase 10 : Préparation Clients (Jour 4 - 1h)
- [ ] Landing page optimisée
- [ ] Onboarding user flow
- [ ] Documentation utilisateur
- [ ] Plan acquisition 5 clients beta

---

## 🔥 JOUR 1 : TESTS BACKEND + FRONTEND (8h)

### Matin : Tests Backend (6h)

#### 1. Configuration Pytest (30min)
```bash
cd backend
pip install pytest pytest-asyncio pytest-cov pytest-mock faker factory-boy
```

Créer `backend/pytest.ini` :
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = 
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=90
    -v
```

Créer `backend/conftest.py` avec fixtures globales.

#### 2. Tests Unitaires Services (3h)

**Ordre de priorité** :
1. `test_auth_service.py` (1h) - Critique
2. `test_invoice_service.py` (45min)
3. `test_transaction_service.py` (45min)
4. `test_bank_service.py` (30min)

**Exemple structure** :
```python
# tests/unit/services/test_auth_service.py
import pytest
from app.services.auth_service import AuthService

@pytest.mark.asyncio
async def test_register_success(db_session):
    """Test successful user registration."""
    user = await AuthService.register(
        db=db_session,
        email="test@example.com",
        password="SecurePass123!",
        company_name="Test Co"
    )
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_verified is False

@pytest.mark.asyncio
async def test_register_duplicate_email(db_session, test_user):
    """Test registration fails with duplicate email."""
    with pytest.raises(ValueError, match="already exists"):
        await AuthService.register(
            db=db_session,
            email=test_user.email,
            password="Password123!",
            company_name="Another Co"
        )

@pytest.mark.asyncio
async def test_login_success(db_session, test_user):
    """Test successful login."""
    tokens = await AuthService.login(
        db=db_session,
        email=test_user.email,
        password="Demo2026!"
    )
    assert "access_token" in tokens
    assert "refresh_token" in tokens

@pytest.mark.asyncio
async def test_login_wrong_password(db_session, test_user):
    """Test login fails with wrong password."""
    with pytest.raises(ValueError, match="Invalid credentials"):
        await AuthService.login(
            db=db_session,
            email=test_user.email,
            password="WrongPassword"
        )
```

#### 3. Tests Unitaires Utils (1h)

- `test_security.py` : hash_password, verify_password, create_token
- `test_validators.py` : email, phone, IBAN validation
- `test_formatters.py` : currency, date formatting

#### 4. Tests Intégration API (1h30)

```python
# tests/integration/test_auth_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.integration
async def test_register_endpoint(client: AsyncClient):
    """Test POST /api/v1/auth/register endpoint."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "company_name": "New Company"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"

@pytest.mark.integration
async def test_login_endpoint(client: AsyncClient):
    """Test POST /api/v1/auth/login endpoint."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "demo@financeai.com",
            "password": "Demo2026!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
```

---

### Après-midi : Tests Frontend (2h)

#### 1. Configuration Vitest (30min)
```bash
cd frontend
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

Créer `frontend/vitest.config.ts` :
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'src/test/'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

#### 2. Tests Composants (1h)
- `InvoiceCard.test.tsx`
- `TransactionList.test.tsx`
- `LoginForm.test.tsx`

#### 3. Tests Hooks (30min)
- `useAuth.test.ts`
- `useInvoices.test.ts`

---

## 🔧 JOUR 2 : QUALITÉ + DATA + MONITORING (7h)

### Matin : Qualité & Linters (2h)

#### 1. Pre-commit hooks (30min)
```bash
pip install pre-commit
```

Créer `.pre-commit-config.yaml` :
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, css]
```

#### 2. Exécuter linters (1h30)
```bash
# Backend
cd backend
black . --line-length 100
ruff check . --fix
mypy app

# Frontend
cd frontend
npm run lint -- --fix
npm run format
```

Fixer toutes les erreurs.

---

### Après-midi : Data + Workers + Monitoring (5h)

#### 1. Seed Data (1h)

Créer `backend/scripts/seed_data.py` :
```python
"""Seed database with realistic demo data."""
import asyncio
from app.database import AsyncSessionLocal
from app.models import User, Invoice, Transaction, BankAccount
from app.services.auth_service import AuthService
from faker import Faker
from decimal import Decimal
import random

fake = Faker('fr_FR')

async def seed():
    async with AsyncSessionLocal() as db:
        # Create 5 demo users
        users = []
        for i in range(5):
            user = await AuthService.register(
                db=db,
                email=f"user{i+1}@demo.com",
                password="Demo2026!",
                company_name=fake.company()
            )
            users.append(user)
        
        # Create bank accounts
        for user in users:
            bank = BankAccount(
                user_id=user.id,
                bank_name=random.choice(["BNP Paribas", "Société Générale", "Crédit Agricole"]),
                account_number=fake.iban(),
                balance=Decimal(random.uniform(5000, 50000))
            )
            db.add(bank)
        
        # Create invoices (100 total)
        for _ in range(100):
            user = random.choice(users)
            invoice = Invoice(
                user_id=user.id,
                client_name=fake.company(),
                amount=Decimal(random.uniform(500, 5000)),
                due_date=fake.date_between(start_date='-30d', end_date='+60d'),
                status=random.choice(['pending', 'paid', 'overdue'])
            )
            db.add(invoice)
        
        await db.commit()
        print("✅ Seed data created successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
```

#### 2. Configuration Redis + Celery (1h)

Mettre à jour `docker-compose.yml` pour inclure Redis.

Créer `backend/app/celery_app.py` proprement configuré.

Tester les workers :
```bash
# Terminal 1
celery -A app.celery_app worker --loglevel=info

# Terminal 2
python -c "from app.workers.bank_sync import sync_bank_transactions; sync_bank_transactions.delay('test-account-id')"
```

#### 3. Monitoring : Sentry (1h)

```bash
pip install sentry-sdk[fastapi]
npm install @sentry/nextjs
```

Configurer dans `backend/app/main.py` :
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    environment=settings.ENVIRONMENT,
    traces_sample_rate=0.1,
)
```

#### 4. Logging Structuré (1h)

```bash
pip install structlog
```

Créer `backend/app/core/logging_config.py` :
```python
import structlog
import logging

def configure_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
```

---

## 🚀 JOUR 3 : CI/CD + DOCUMENTATION (5h)

### Matin : CI/CD (3h)

Créer `.github/workflows/ci.yml` :
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
      - name: Run tests
        run: |
          cd backend
          pytest --cov --cov-fail-under=90
      - name: Run linters
        run: |
          cd backend
          black --check .
          ruff check .
          mypy app

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm run test:coverage
      - name: Run linters
        run: |
          cd frontend
          npm run lint
          npm run type-check

  build-docker:
    needs: [backend-tests, frontend-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Build images
        run: docker-compose build
```

---

### Après-midi : Documentation (2h)

#### 1. README.md principal (45min)

Structure :
```markdown
# FinanceAI - Automatisation Comptable PME

## 🎯 Qu'est-ce que c'est ?
## ⚡ Fonctionnalités
## 🚀 Quick Start
## 📚 Documentation
## 🧪 Tests
## 🔒 Sécurité
## 📄 Licence
```

#### 2. SETUP.md (30min)

Guide d'installation détaillé :
- Prérequis
- Installation locale
- Docker Compose
- Variables d'environnement
- Base de données
- Seed data

#### 3. ARCHITECTURE.md (30min)

Décisions techniques :
- Pourquoi FastAPI ?
- Pourquoi Next.js ?
- Structure du code
- Flux de données
- Authentification
- API externes

#### 4. Nettoyage (15min)

Supprimer documents obsolètes :
- `PLAN_DEV_IMMEDIAT.md`
- `MAKE_WORKFLOWS_SETUP.md`
- `DEMARRAGE_IMMEDIAT.md`
- `WEEK1_DONE.md`
- Anciens fichiers de débogage

---

## 🎨 JOUR 4 : OPTIMISATION + DÉPLOIEMENT (6h)

### Matin : Optimisations (2h)

#### 1. Database (1h)
- Ajouter indexes manquants
- Optimiser queries N+1
- Tester performance

#### 2. Frontend (1h)
- Code splitting
- Image optimization
- Bundle size analysis

---

### Après-midi : Déploiement (4h)

#### 1. Configuration Production (1h)
- Variables d'environnement
- Secrets management
- SSL certificates

#### 2. Deploy Backend (1h)
- Railway / Render / AWS
- PostgreSQL production
- Redis production

#### 3. Deploy Frontend (1h)
- Vercel / Netlify
- Environment variables
- Domain configuration

#### 4. Tests Production (1h)
- Smoke tests
- E2E tests sur prod
- Monitoring check

---

## ✅ DÉFINITION OF DONE

Le projet sera considéré "fini proprement" quand :

### Tests
- [ ] 90%+ couverture backend (pytest-cov)
- [ ] 80%+ couverture frontend (vitest)
- [ ] Tous les tests passent
- [ ] Tests CI/CD passent

### Qualité
- [ ] Black, Ruff, mypy : 0 erreurs
- [ ] ESLint, Prettier : 0 erreurs
- [ ] Pre-commit hooks configurés
- [ ] Docstrings complètes

### Fonctionnalités
- [ ] Tous les endpoints fonctionnels
- [ ] Seed data opérationnel
- [ ] Celery workers fonctionnels
- [ ] Monitoring actif (Sentry)

### Documentation
- [ ] README.md complet
- [ ] SETUP.md détaillé
- [ ] ARCHITECTURE.md clair
- [ ] Code commenté (logique complexe)

### Déploiement
- [ ] Backend en production
- [ ] Frontend en production
- [ ] CI/CD opérationnel
- [ ] Monitoring production actif

---

## 🎯 APRÈS LA FINITION

Une fois tout propre, focus sur **l'acquisition** :

### Semaine 1-2 : Premiers Clients
- [ ] Contacter 20 PME ciblées
- [ ] Offrir 1 mois gratuit
- [ ] Onboarding assisté
- [ ] Feedback sessions

### Objectif
**5 clients beta payants à 50€/mois = 250€ MRR**

---

**Auteur** : AI Assistant  
**Date** : 5 janvier 2026 - 23:30  
**Status** : 🟢 Roadmap prête - On commence maintenant !

