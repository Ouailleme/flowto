# 🚀 FinanceAI - Automatisation Comptable PME

**Stack 2026**: Python FastAPI + Next.js 15 + PostgreSQL + Redis + Celery + IA

---

## 🎯 Projet

Application SaaS d'automatisation comptable pour PME avec IA:
- 🏦 Connexion bancaire automatique (Bridge API)
- 🤖 Catégorisation transactions par IA (Claude 3.5)
- 🔄 Rapprochement bancaire automatique
- 📧 Relances clients intelligentes
- 📊 Prévision trésorerie

---

## 🏗️ Architecture

```
financeai/
├── backend/          # Python 3.12 + FastAPI + SQLAlchemy + Celery
├── frontend/         # Next.js 15 + TypeScript + shadcn/ui
├── docker-compose.yml
└── docs/
```

**Stack**:
- **Backend**: FastAPI (async), PostgreSQL, Redis, Celery
- **Frontend**: Next.js 15, TypeScript, TanStack Query, Zustand
- **IA**: Claude 3.5 Sonnet (catégorisation + matching + emails)
- **APIs**: Bridge (banques), SendGrid (emails)
- **DevOps**: Docker, GitHub Actions, Railway/Fly.io

---

## 🚀 Quick Start

### Prérequis
- Docker Desktop
- Python 3.12+
- Node.js 20+
- Git

### Lancer l'app (Docker Compose)

```bash
# 1. Cloner le repo
git clone <repo-url>
cd financeai

# 2. Copier les variables d'environnement
cp backend/env.template backend/.env
cp frontend/env.local.template frontend/.env.local

# 3. Éditer backend/.env avec tes clés API:
# - BRIDGE_API_KEY
# - ANTHROPIC_API_KEY
# - SENDGRID_API_KEY
# - SECRET_KEY (générer: openssl rand -base64 32)

# 4. Lancer tout
docker-compose up

# 5. Accéder:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Développement manuel (sans Docker)

```bash
# Terminal 1: Database + Redis
docker-compose up postgres redis

# Terminal 2: Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp env.template .env
# Éditer .env
uvicorn app.main:app --reload

# Terminal 3: Celery Worker
cd backend
source venv/bin/activate
celery -A app.workers.celery_app worker --loglevel=info

# Terminal 4: Frontend
cd frontend
npm install
cp env.local.template .env.local
npm run dev
```

---

## 📚 Documentation

### Pour démarrer le développement:
👉 **Lis d'abord**: [`START_DEVELOPMENT.md`](START_DEVELOPMENT.md)

### Plan complet (2 semaines):
👉 [`PLAN_DEV_CODE_FIRST.md`](PLAN_DEV_CODE_FIRST.md)

### Standards de qualité:
👉 [`.cursorrules`](.cursorrules) (Sécurité, Tests, Code quality)

### Recherche & Validation (✅ Complète):
- [`RAPPORT_FINAL_RECHERCHE_IA_2026.md`](RAPPORT_FINAL_RECHERCHE_IA_2026.md) - Analyse marché
- [`ROADMAP_FINANCE_PME.md`](ROADMAP_FINANCE_PME.md) - Roadmap long terme
- [`matrice_evaluation_niches.md`](matrice_evaluation_niches.md) - 10 niches évaluées

---

## 🎯 Roadmap Développement

### ✅ Phase 0: Recherche & Validation (FAIT)
- Analyse marché IA 2026
- Identification 30+ pain points
- Évaluation 10 niches
- Sélection niche: **Finance PME** (score 94/100)

### 🔥 Phase 1: MVP Full-Code (EN COURS - 2 semaines)

**Semaine 1: Backend**
- [x] Setup infrastructure (Docker, PostgreSQL, Redis)
- [x] Configuration FastAPI + SQLAlchemy
- [ ] Auth système (JWT, User model)
- [ ] CRUD de base (Bank, Transaction, Invoice)
- [ ] Intégrations (Bridge, Claude, SendGrid)
- [ ] Celery workers (sync, reconciliation, reminders)
- [ ] Tests (90%+ coverage)

**Semaine 2: Frontend**
- [ ] Setup Next.js 15 + TypeScript
- [ ] Pages (Login, Dashboard, Banks, Transactions, Invoices)
- [ ] API client + TanStack Query
- [ ] UI/UX avec shadcn/ui
- [ ] Tests E2E (Playwright)

### Phase 2: Beta Test (Semaines 3-4)
- [ ] Déploiement production (Railway)
- [ ] 5 early adopters
- [ ] Collecte feedback
- [ ] Itérations rapides

### Phase 3: Scale (Semaines 5-8)
- [ ] Optimisations performance
- [ ] Features avancées (exports, analytics)
- [ ] Monitoring & alerting
- [ ] Acquisition clients (10+ payants)

---

## 🧪 Tests

```bash
# Backend
cd backend
pytest --cov=app --cov-report=html
# Ouvrir: htmlcov/index.html

# Frontend
cd frontend
npm run test
npm run test:e2e
```

**Target**: 90%+ coverage backend, 80%+ frontend

---

## 🔒 Sécurité

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ Input validation (Pydantic)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CORS configuré
- ✅ Rate limiting (TODO)
- ✅ Audit logs (toutes actions critiques)
- ✅ HTTPS only (production)
- ✅ Secrets management (env variables)

**Conformité**: RGPD, PCI-DSS (pas de stockage direct IBAN/CB)

---

## 🚢 Déploiement

### Production (Railway)

```bash
# Backend
railway up

# Frontend (Vercel)
vercel deploy --prod

# Database: Supabase (PostgreSQL)
# Redis: Railway Redis plugin
```

### Variables d'environnement requises

**Backend**:
- `DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `BRIDGE_API_KEY`
- `ANTHROPIC_API_KEY`
- `SENDGRID_API_KEY`

**Frontend**:
- `NEXT_PUBLIC_API_URL`

---

## 📊 Monitoring

- **Errors**: Sentry
- **Logs**: Structured JSON logging
- **Metrics**: TODO (Prometheus + Grafana)
- **Uptime**: Railway health checks

---

## 🤝 Contribution

Ce projet suit des standards stricts (voir `.cursorrules`):
- Tests obligatoires (90%+ coverage)
- Linting (Black, Ruff, ESLint)
- Type checking (mypy, TypeScript strict)
- Code review obligatoire

---

## 📝 Licence

Propriétaire (pour l'instant)

---

## 📞 Contact

- **Développeurs**: Les meilleurs de 2026 💪
- **Stack**: Le meilleur de 2026 🔥
- **Objectif**: Produit le plus scalable et sécurisé du marché 🚀

---

**Let's build! 💻**
