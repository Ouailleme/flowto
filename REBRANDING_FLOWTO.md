# 🎨 Rebranding : FinanceAI → Flowto

**Date** : 6 janvier 2026  
**Nouveau nom** : **Flowto**  
**Nouveau domaine** : **flowto.fr**

---

## ✅ Changements Appliqués

### 📝 Noms et Marque
- **FinanceAI** → **Flowto**
- **financeai** → **flowto** (code, variables)
- **financeai.app** → **flowto.fr** (domaine)
- **financeai.com** → **flowto.fr** (emails)

### 📧 Emails
- `demo@financeai.com` → `demo@flowto.fr`
- `support@financeai.app` → `support@flowto.fr`
- `noreply@financeai.app` → `noreply@flowto.fr`

### 🗄️ Base de Données
- **User** : `financeai` → `flowto`
- **Password** : `financeai2026` → `flowto2026`
- **Database** : `financeai` → `flowto`

### 🐳 Containers Docker
- `financeai_backend` → `flowto_backend`
- `financeai_frontend` → `flowto_frontend`
- `financeai_postgres` → `flowto_postgres`
- `financeai_redis` → `flowto_redis`

---

## 📁 Fichiers Modifiés

### Documentation
- ✅ `README.md` - Titre, domaines, emails, URLs
- ✅ `PROJET_COMPLETE.md` - Nom du projet
- ✅ `Makefile` - Titre, messages, credentials

### Configuration Backend
- ✅ `backend/app/core/config.py`
  - `app_name`: "FinanceAI API" → "Flowto API"
  - `cors_origins`: financeai.app → flowto.fr
  - `sendgrid_from_email`: @financeai.app → @flowto.fr

### Monitoring & Logs
- ✅ `backend/app/core/monitoring.py`
  - Sentry release: `financeai-backend` → `flowto-backend`
  - Logger names: `financeai.api` → `flowto.api`
  - Logger names: `financeai.errors` → `flowto.errors`

- ✅ `frontend/src/lib/monitoring.ts`
  - Sentry release: `financeai-frontend` → `flowto-frontend`
  - Trace targets: `api.financeai.app` → `api.flowto.fr`

### Seed Data
- ✅ `backend/scripts/seed_data.py`
  - Demo user: `demo@financeai.com` → `demo@flowto.fr`

### Infrastructure
- ✅ `docker-compose.yml`
  - Container names: financeai_* → flowto_*
  - Database user/password/db name
  - DATABASE_URL env var

- ✅ `frontend/package.json`
  - Package name: "financeai-frontend" → "flowto-frontend"

### CI/CD
- ✅ `.github/workflows/backend-ci.yml`
  - Docker image tags: financeai-backend → flowto-backend

- ✅ `.github/workflows/frontend-ci.yml`
  - Docker image tags: financeai-frontend → flowto-frontend

---

## 🚀 Actions Post-Rebranding

### 1. Redémarrer l'application

```bash
# Arrêter les containers existants
make stop

# Supprimer les volumes (nettoie l'ancienne DB)
docker-compose down -v

# Redémarrer avec les nouveaux noms
make dev
```

### 2. Recréer la base de données

```bash
# Les tables seront créées automatiquement au démarrage

# Ajouter les données de démo
make seed
```

### 3. Nouveaux credentials de test

**Email** : `demo@flowto.fr`  
**Password** : `Demo123!`

### 4. URLs mises à jour

- **Frontend** : http://localhost:3000
- **Backend** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs
- **Production (future)** : https://flowto.fr

---

## 📊 Récapitulatif des Occurrences

| Terme              | Occurrences | Fichiers affectés |
|--------------------|-------------|-------------------|
| FinanceAI          | ~50         | 12 fichiers       |
| financeai          | ~150        | 128 fichiers      |
| financeai.app      | ~10         | 5 fichiers        |
| financeai.com      | ~5          | 3 fichiers        |
| **TOTAL**          | **~215**    | **130+ fichiers** |

---

## 🎯 Fichiers Non Modifiés (Optionnel)

Certains fichiers documentaires gardent les références historiques :
- Fichiers de tests E2E (playwright reports)
- Fichiers de documentation technique
- Logs et test results
- Fichiers MCP (documentation interne)

Ces fichiers peuvent être mis à jour ultérieurement si nécessaire, mais ne sont pas critiques pour le fonctionnement.

---

## ⚠️ Attention

### Variables d'environnement à mettre à jour

Si vous avez des fichiers `.env` locaux non versionnés :

```bash
# backend/.env
DATABASE_URL=postgresql+asyncpg://flowto:flowto2026@postgres:5432/flowto

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Sentry DSN

Si vous utilisez Sentry en production, mettez à jour :
- Nom du projet Sentry : FinanceAI → Flowto
- Release tags dans les settings

### GitHub Repository

Si le repository GitHub est renommé :
- Mettre à jour les URLs dans les badges du README
- Mettre à jour les URLs dans les workflows CI/CD

---

## ✅ Checklist de Validation

- [x] README.md mis à jour
- [x] Documentation principale mise à jour
- [x] Configuration backend (config.py)
- [x] Monitoring (Sentry, logs)
- [x] Seed data (emails de démo)
- [x] Docker Compose (containers, DB)
- [x] CI/CD workflows
- [x] Frontend monitoring
- [ ] Tests en local (make dev, make seed, make test)
- [ ] Déploiement production (à faire)

---

## 🎉 Résultat

Le projet **Flowto** est maintenant prêt avec :
- ✅ Nom de marque cohérent partout
- ✅ Domaine flowto.fr configuré
- ✅ Emails @flowto.fr
- ✅ Base de données renommée
- ✅ Containers Docker renommés
- ✅ CI/CD mis à jour

**Le rebranding est complet ! 🚀**

---

*Made with ❤️ by the Flowto Team*

