# 💰 Flowto - Automatisation Comptable pour PME

<div align="center">

[![Backend CI](https://img.shields.io/github/workflow/status/your-org/flowto/Backend%20CI?label=backend&logo=fastapi)](https://github.com/your-org/flowto/actions)
[![Frontend CI](https://img.shields.io/github/workflow/status/your-org/flowto/Frontend%20CI?label=frontend&logo=next.js)](https://github.com/your-org/flowto/actions)
[![E2E Tests](https://img.shields.io/github/workflow/status/your-org/flowto/E2E%20Tests?label=e2e&logo=playwright)](https://github.com/your-org/flowto/actions)
[![codecov](https://codecov.io/gh/your-org/flowto/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/flowto)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)

**Plateforme SaaS FinTech pour automatiser la comptabilité des PME**

[Demo](https://flowto.fr) • [Documentation](docs/) • [API Docs](http://localhost:8000/docs) • [Report Bug](https://github.com/your-org/flowto/issues)

</div>

---

## 📋 Table des matières

- [✨ Fonctionnalités](#-fonctionnalités)
- [🚀 Quick Start](#-quick-start)
- [🏗️ Architecture](#%EF%B8%8F-architecture)
- [🧪 Tests](#-tests)
- [📊 Monitoring](#-monitoring)
- [🔒 Sécurité](#-sécurité)
- [🛠️ Développement](#%EF%B8%8F-développement)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Fonctionnalités

### 🏦 Rapprochement Bancaire Automatisé
- Synchronisation temps réel avec 400+ banques (Bridge API)
- Catégorisation intelligente des transactions (Claude AI)
- Rapprochement automatique factures ↔ transactions
- Détection des anomalies et doublons

### 📄 Gestion des Factures
- Création et suivi des factures clients
- Relances automatiques (emails programmables)
- Tracking des paiements en retard
- Export PDF professionnel

### 📈 Prévisions Trésorerie
- Analyse des flux de trésorerie
- Prédictions basées sur l'historique
- Alertes de trésorerie faible
- Visualisations interactives

### 🤖 Intelligence Artificielle
- Catégorisation automatique des dépenses (Claude)
- Suggestions de réconciliation
- Détection d'anomalies
- Insights financiers personnalisés

### 🔐 Sécurité & Conformité
- Chiffrement end-to-end
- Authentification 2FA
- Audit trail complet
- Conformité RGPD & PCI-DSS

---

## 🚀 Quick Start

### Prérequis

- [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)
- [Make](https://www.gnu.org/software/make/) (optionnel, pour les commandes simplifiées)

### Installation en 3 étapes

```bash
# 1. Cloner le repository
git clone https://github.com/your-org/flowto.git
cd flowto

# 2. Configurer les variables d'environnement
cp backend/.env.example backend/.env
cp frontend/.env.local.template frontend/.env.local

# 3. Démarrer l'application
make dev
# Ou sans Make: docker-compose up -d
```

🎉 **C'est tout !** L'application est accessible sur :
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs

### Données de démonstration

```bash
# Ajouter des données de test
make seed

# Credentials de démo
Email: demo@flowto.fr
Password: Demo123!
```

---

## 🏗️ Architecture

```
flowto/
├── backend/              # API FastAPI (Python 3.12)
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   ├── workers/     # Celery tasks
│   │   └── integrations/ # External APIs
│   ├── tests/           # Tests (pytest)
│   └── alembic/         # Database migrations
│
├── frontend/            # Next.js 15 (React, TypeScript)
│   ├── src/
│   │   ├── app/         # App Router pages
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   └── lib/         # Utilities
│   └── e2e/             # E2E tests (Playwright)
│
├── .github/
│   └── workflows/       # CI/CD pipelines
│
└── docker-compose.yml   # Services orchestration
```

### Stack Technique

**Backend**
- **Framework** : FastAPI (Python 3.12)
- **Database** : PostgreSQL 17 + asyncpg
- **Cache** : Redis 7
- **ORM** : SQLAlchemy (async)
- **Task Queue** : Celery
- **Auth** : JWT + bcrypt
- **Validation** : Pydantic
- **Testing** : pytest + pytest-cov
- **Monitoring** : Sentry + structlog

**Frontend**
- **Framework** : Next.js 15 (App Router)
- **Language** : TypeScript 5
- **UI** : shadcn/ui + Tailwind CSS 3
- **State** : React Query (TanStack)
- **Forms** : React Hook Form + Zod
- **Charts** : Recharts
- **Testing** : Playwright

**Infrastructure**
- **Containers** : Docker + Docker Compose
- **CI/CD** : GitHub Actions
- **Monitoring** : Sentry
- **Logs** : structlog (JSON)

**Intégrations Externes**
- **Banking** : Bridge API (400+ banques)
- **AI** : Claude 3.5 Sonnet (Anthropic)
- **Email** : SendGrid

---

## 🧪 Tests

### Tests Backend

```bash
# Tous les tests avec coverage
make test-backend

# Tests rapides (sans coverage)
make test-backend-fast

# Coverage HTML
make test-coverage
```

**Couverture actuelle : 90%+**

```
Tests Suite               Tests    Coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Smoke Tests                   7      100%
AuthService                  36       98%
InvoiceService               29      100%
API Auth                      9      100%
API Invoices                 12      100%
API Transactions              7       95%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL                       100       92%
```

### Tests E2E

```bash
# Lancer les tests E2E
make test-e2e

# Ou avec l'interface Playwright
cd frontend && npx playwright test --ui
```

---

## 📊 Monitoring

### Sentry (Error Tracking)

```bash
# Backend
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# Frontend
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### Logging Structuré (JSON)

Les logs sont au format JSON pour faciliter l'analyse :

```json
{
  "timestamp": "2026-01-05T23:45:12Z",
  "level": "info",
  "logger": "flowto.api",
  "event": "http_request",
  "method": "POST",
  "path": "/api/v1/invoices",
  "status_code": 201,
  "duration_ms": 45,
  "user_id": "uuid-here"
}
```

### Health Checks

```bash
# Vérifier l'état des services
make health

# Résultat attendu:
Backend:  ✓ Healthy
Frontend: ✓ Healthy
Database: ✓ Healthy
Redis:    ✓ Healthy
```

---

## 🔒 Sécurité

### Authentification

- JWT avec refresh tokens
- Tokens stockés en httpOnly cookies
- Expiration : 1h (access) / 30 jours (refresh)
- CSRF protection activée
- Rate limiting : 10 req/min sur `/auth/login`

### Données Sensibles

- Mots de passe : bcrypt (cost 12)
- IBAN/Données bancaires : chiffrement AES-256
- Secrets : variables d'environnement + HashiCorp Vault (prod)

### RGPD

- Consentement explicite
- Export des données utilisateur
- Suppression compte (soft delete)
- Audit trail complet

### Audit

Toutes les actions critiques sont loggées :
- Authentification (login, logout, changement MDP)
- Opérations financières (factures, transactions)
- Modifications de données
- Accès API

---

## 🛠️ Développement

### Commandes principales

```bash
# Développement
make dev              # Démarrer l'app
make stop             # Arrêter l'app
make restart          # Redémarrer
make logs             # Voir les logs

# Base de données
make db-migrate       # Migrations
make db-rollback      # Rollback
make seed             # Seed data

# Code Quality
make lint             # Linter
make format           # Formater
make test             # Tests

# Outils
make shell-backend    # Shell backend
make shell-db         # Shell PostgreSQL
make help             # Voir toutes les commandes
```

### Structure des commits

Utiliser [Conventional Commits](https://www.conventionalcommits.org/) :

```
feat: Add invoice PDF export
fix: Fix transaction categorization bug
docs: Update API documentation
test: Add tests for AuthService
refactor: Simplify invoice service logic
chore: Update dependencies
```

### Branches

- `main` : Production (protégée)
- `develop` : Développement
- `feature/*` : Nouvelles features
- `fix/*` : Bug fixes
- `hotfix/*` : Hotfixes production

---

## 📚 Documentation

- **Architecture** : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **API Reference** : http://localhost:8000/docs (Swagger)
- **Deployment** : [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Contributing** : [CONTRIBUTING.md](CONTRIBUTING.md)
- **Changelog** : [CHANGELOG.md](CHANGELOG.md)

---

## 🤝 Contributing

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'feat: Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

### Code of Conduct

Nous suivons le [Contributor Covenant](https://www.contributor-covenant.org/). Soyez respectueux et inclusif.

---

## 🙏 Remerciements

- [FastAPI](https://fastapi.tiangolo.com/) pour le framework backend
- [Next.js](https://nextjs.org/) pour le framework frontend
- [shadcn/ui](https://ui.shadcn.com/) pour les composants UI
- [Bridge API](https://bridgeapi.io/) pour l'agrégation bancaire
- [Anthropic](https://www.anthropic.com/) pour Claude AI

---

## 📄 License

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Équipe

**Maintainers**

- [@yvesm](https://github.com/yvesm) - Creator & Lead Developer

**Contributors**

Voir la liste complète des [contributors](https://github.com/your-org/flowto/contributors).

---

## 📞 Support

- 📧 Email : support@flowto.fr
- 💬 Discord : [Join our community](https://discord.gg/flowto)
- 🐛 Issues : [GitHub Issues](https://github.com/your-org/flowto/issues)
- 📖 Docs : [Documentation](docs/)

---

<div align="center">

**Made with ❤️ by the Flowto Team**

⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile !

</div>
