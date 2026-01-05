# 🚀 FinanceAI - Guide de Démarrage Rapide

## 📋 Prérequis

- **Docker** & **Docker Compose** installés
- **Node.js** 18+ (pour le frontend)
- **Python** 3.11+ (pour le backend)
- **Git** (optionnel)

---

## ⚡ DÉMARRAGE RAPIDE (5 minutes)

### **1. Lancer les services Docker**

```bash
# Depuis la racine du projet
docker-compose up -d postgres redis

# Vérifier que ça tourne
docker-compose ps
```

### **2. Setup Backend**

```bash
cd backend

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer dependencies
pip install -r requirements.txt

# Copier le fichier env
cp env.template .env

# IMPORTANT: Éditer .env et remplir:
# - DATABASE_URL (déjà configuré pour Docker)
# - CLAUDE_API_KEY (optionnel pour MVP)
# - SENDGRID_API_KEY (optionnel pour MVP)
# - BRIDGE_API_KEY (optionnel pour MVP)

# Initialiser la base de données
python scripts/init_db.py

# ✅ La DB est créée avec des données de démo !

# Lancer le serveur
uvicorn app.main:app --reload

# 🎉 Backend lancé sur http://localhost:8000
```

### **3. Setup Frontend**

```bash
# Nouveau terminal
cd frontend

# Installer dependencies
npm install

# Copier env
cp env.local.template .env.local

# Éditer .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000

# Lancer le dev server
npm run dev

# 🎉 Frontend lancé sur http://localhost:3000
```

### **4. Tester l'application**

1. **Ouvrir** http://localhost:3000
2. **Se connecter** avec les credentials démo:
   - Email: `demo@financeai.com`
   - Password: `demo123`
3. **Explorer** le dashboard ! 🚀

---

## 🧪 TESTS

### Backend
```bash
cd backend

# Lancer les tests
pytest

# Avec coverage
pytest --cov=app --cov-report=html

# Ouvrir le rapport
open htmlcov/index.html
```

### Frontend
```bash
cd frontend

# Lancer en mode dev
npm run dev

# Build production
npm run build
```

---

## 📊 ALEMBIC MIGRATIONS

### Créer une migration
```bash
cd backend

# Après modification des models
alembic revision --autogenerate -m "Description des changements"

# Appliquer les migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 🔧 SCRIPTS UTILES

### Backend Dev Server
```bash
cd backend
./scripts/dev.sh
# Démarre PostgreSQL + Redis + Migrations + FastAPI
```

### Tests Backend
```bash
cd backend
./scripts/run_tests.sh
# Lance pytest avec coverage
```

### Initialiser DB avec données démo
```bash
cd backend
python scripts/init_db.py
```

---

## 🐳 DOCKER COMMANDES

```bash
# Tout lancer
docker-compose up -d

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f

# Réinitialiser la DB
docker-compose down -v
docker-compose up -d postgres
cd backend && python scripts/init_db.py
```

---

## 📁 STRUCTURE PROJET

```
FinanceAI/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── models/          # 7 models SQLAlchemy
│   │   ├── services/        # 8 services métier
│   │   ├── api/v1/          # 15+ endpoints
│   │   ├── integrations/    # Bridge, Claude, SendGrid
│   │   └── workers/         # 5 Celery tasks
│   ├── alembic/             # Migrations
│   ├── scripts/             # Scripts utiles
│   └── tests/               # 50+ tests (90%+ coverage)
│
├── frontend/                # Next.js 15 Frontend
│   ├── src/
│   │   ├── app/             # Pages (Next.js App Router)
│   │   ├── components/      # UI components
│   │   ├── hooks/           # React hooks (TanStack Query)
│   │   └── lib/             # API client + utils
│   └── package.json
│
└── docker-compose.yml       # PostgreSQL + Redis
```

---

## 🌐 URLs IMPORTANTES

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Postgres**: localhost:5432 (user: postgres, pass: postgres, db: financeai)
- **Redis**: localhost:6379

---

## 🔑 CREDENTIALS DÉMO

**Email**: `demo@financeai.com`  
**Password**: `demo123`

**Données incluses**:
- 1 compte bancaire (BNP Paribas)
- 7 transactions (catégorisées)
- 4 factures (pending, paid, overdue)

---

## 🚨 TROUBLESHOOTING

### Port déjà utilisé
```bash
# Backend (8000)
lsof -ti:8000 | xargs kill -9

# Frontend (3000)
lsof -ti:3000 | xargs kill -9
```

### Base de données corrompue
```bash
docker-compose down -v
docker-compose up -d postgres
cd backend && python scripts/init_db.py
```

### Modules Python manquants
```bash
cd backend
pip install -r requirements.txt
```

### Modules npm manquants
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🎯 PROCHAINES ÉTAPES

1. **Tester l'application** avec les données démo
2. **Explorer l'API** via Swagger (http://localhost:8000/docs)
3. **Modifier les models** et créer des migrations
4. **Ajouter des features** (pages, endpoints, etc.)
5. **Déployer** sur Railway/Vercel

---

## 📖 DOCUMENTATION COMPLÈTE

- **Architecture**: `DEVELOPMENT_SUMMARY.md`
- **Roadmap**: `ROADMAP_FINANCE_PME.md`
- **Design System**: `DESIGN_SYSTEM_2026.md`
- **Business Model**: `modele_economique_projections.md`
- **Tests**: `tests/README.md`

---

## 💬 BESOIN D'AIDE ?

- **Swagger UI**: http://localhost:8000/docs
- **Code Coverage**: Après `pytest --cov`, ouvrir `htmlcov/index.html`
- **Logs Backend**: Terminal où `uvicorn` tourne
- **Logs Frontend**: Terminal où `npm run dev` tourne

---

**🎉 Bon développement ! Tu as tout ce qu'il faut pour lancer ton SaaS FinTech ! 🚀**


