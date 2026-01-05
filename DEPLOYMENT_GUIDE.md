# 🚀 Guide de Déploiement - FinanceAI

## 📋 Options de Déploiement

### Option 1: **Railway** (Recommandé - Le plus simple)
### Option 2: **Fly.io** (Plus flexible)
### Option 3: **DigitalOcean / AWS** (Contrôle total)

---

## 🚂 OPTION 1: RAILWAY (15 minutes)

### **Avantages**
- ✅ Setup le plus simple
- ✅ PostgreSQL & Redis inclus
- ✅ Déploiement automatique depuis GitHub
- ✅ $5/mois pour commencer
- ✅ SSL automatique

### **Étapes**

#### **1. Créer compte Railway**
```bash
# Installer CLI
npm install -g @railway/cli

# Login
railway login
```

#### **2. Créer projet**
```bash
# Depuis la racine du projet
railway init

# Nom: financeai
```

#### **3. Ajouter PostgreSQL**
```bash
railway add postgres
```

#### **4. Ajouter Redis**
```bash
railway add redis
```

#### **5. Configurer Backend**
```bash
cd backend

# Créer Dockerfile (déjà fait !)
# Déployer
railway up
```

**Variables d'env Railway (Dashboard):**
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=your-secret-key-here
CLAUDE_API_KEY=your-claude-key
SENDGRID_API_KEY=your-sendgrid-key
BRIDGE_API_KEY=your-bridge-key
CORS_ORIGINS=https://your-frontend.vercel.app
```

#### **6. Configurer Frontend (Vercel)**
```bash
# Via dashboard Vercel
1. Connecter GitHub repo
2. Root directory: frontend/
3. Build command: npm run build
4. Output directory: .next

# Variables d'env:
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## ✈️ OPTION 2: FLY.IO

### **Avantages**
- ✅ Plus flexible que Railway
- ✅ Machines virtuelles complètes
- ✅ Gratuit pour petits projets
- ✅ Déploiement global

### **Étapes**

#### **1. Installer Fly CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

#### **2. Login**
```bash
fly auth login
```

#### **3. Déployer Backend**
```bash
cd backend

# Créer app
fly launch
# Nom: financeai-api
# Region: Paris (cdg)

# Ajouter PostgreSQL
fly postgres create
# Nom: financeai-db

# Attacher à l'app
fly postgres attach financeai-db

# Ajouter Redis
fly redis create
# Nom: financeai-redis

# Secrets
fly secrets set SECRET_KEY=your-secret-key
fly secrets set CLAUDE_API_KEY=your-key
fly secrets set SENDGRID_API_KEY=your-key
fly secrets set BRIDGE_API_KEY=your-key

# Déployer
fly deploy
```

#### **4. Déployer Frontend (Vercel)**
Même chose que Railway

---

## 🔧 CONFIGURATION CELERY WORKERS

### **Railway**
```bash
# Créer service séparé pour Celery
railway add

# Nom: financeai-worker
# Utiliser même Dockerfile backend
# Command: celery -A app.workers.celery_app worker -l info

# Ajouter Celery Beat (scheduler)
railway add
# Nom: financeai-beat
# Command: celery -A app.workers.celery_app beat -l info
```

### **Fly.io**
```toml
# fly.toml
[processes]
  web = "uvicorn app.main:app --host 0.0.0.0 --port 8080"
  worker = "celery -A app.workers.celery_app worker -l info"
  beat = "celery -A app.workers.celery_app beat -l info"
```

---

## 🌐 DOMAINE PERSONNALISÉ

### **Backend (Railway/Fly)**
```bash
# Railway
railway domain add api.financeai.com

# Fly.io
fly certs add api.financeai.com
```

### **Frontend (Vercel)**
```bash
# Via dashboard Vercel
Settings > Domains > Add domain
# financeai.com
```

### **DNS (Cloudflare recommandé)**
```
A     @           76.76.21.21 (Vercel)
CNAME api         your-app.railway.app
CNAME www         financeai.com
```

---

## 📊 MIGRATIONS PRODUCTION

### **Avant chaque déploiement**
```bash
# Local: Créer migration
alembic revision --autogenerate -m "Add feature X"

# Commit & push
git add alembic/versions/*
git commit -m "Migration: Add feature X"
git push

# Sur Railway/Fly, ajouter release command:
# Railway: Settings > Deploy > Release Command
release_command = "alembic upgrade head"

# Fly.io: fly.toml
[deploy]
  release_command = "alembic upgrade head"
```

---

## 🔒 SÉCURITÉ PRODUCTION

### **Variables d'environnement**
```bash
# JAMAIS commiter:
# - .env
# - .env.local
# - API keys

# Toujours utiliser:
# - Railway Secrets
# - Fly Secrets
# - Vercel Environment Variables
```

### **CORS**
```python
# backend/app/main.py
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # PAS "*" en prod !
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Rate Limiting**
```bash
# Ajouter slowapi
pip install slowapi

# backend/app/main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/invoices")
@limiter.limit("100/minute")
async def list_invoices():
    ...
```

---

## 📈 MONITORING

### **Sentry (Error Tracking)**
```bash
# Backend
pip install sentry-sdk[fastapi]

# frontend
npm install @sentry/nextjs

# Init
sentry-sdk.init(
    dsn="YOUR_SENTRY_DSN",
    environment="production"
)
```

### **Uptime Monitoring**
- **UptimeRobot** (gratuit)
- **BetterUptime** (gratuit)
- Ping toutes les 5 min: https://api.financeai.com/health

---

## 💰 COÛTS ESTIMÉS

### **MVP (0-100 utilisateurs)**
```
Railway Backend:       $5-10/mois
Railway PostgreSQL:    $5/mois
Railway Redis:         $5/mois
Vercel Frontend:       $0 (gratuit)
-------------------------------------
TOTAL:                 $15-20/mois
```

### **Growth (100-1000 utilisateurs)**
```
Railway/Fly:           $50-100/mois
Vercel Pro:            $20/mois
Sentry:                $26/mois
-------------------------------------
TOTAL:                 $96-146/mois
```

### **Scale (1000+ utilisateurs)**
```
AWS/GCP/DigitalOcean:  $200-500/mois
CDN (Cloudflare):      $20/mois
Monitoring:            $50/mois
-------------------------------------
TOTAL:                 $270-570/mois
```

---

## ✅ CHECKLIST PRÉ-DÉPLOIEMENT

### **Backend**
- [ ] Tests passent (`pytest`)
- [ ] Coverage > 90%
- [ ] `.env` pas commité
- [ ] CORS configuré
- [ ] Rate limiting activé
- [ ] Logging configuré
- [ ] Sentry configuré
- [ ] Migrations testées

### **Frontend**
- [ ] Build réussit (`npm run build`)
- [ ] `.env.local` pas commité
- [ ] API_URL configuré
- [ ] Error boundaries
- [ ] Loading states
- [ ] SEO metadata

### **Database**
- [ ] Backups automatiques (Railway/Fly)
- [ ] Indexes créés
- [ ] Migrations réversibles

### **Monitoring**
- [ ] Sentry configuré
- [ ] Uptime monitoring
- [ ] Logs centralisés
- [ ] Alertes configurées

---

## 🚨 ROLLBACK PLAN

### **Si déploiement échoue**
```bash
# Railway
railway rollback

# Fly.io
fly releases list
fly releases rollback v123

# Vercel
# Via dashboard: Deployments > Previous > Promote to Production
```

### **Si migration échoue**
```bash
# SSH dans le container
railway run bash  # ou fly ssh console

# Rollback migration
alembic downgrade -1

# Fix & redéployer
```

---

## 📞 SUPPORT

### **Railway**
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app

### **Fly.io**
- Community: https://community.fly.io
- Docs: https://fly.io/docs

### **Vercel**
- Discord: https://vercel.com/discord
- Docs: https://vercel.com/docs

---

**🎉 Bon déploiement ! Tu vas cartonner ! 🚀**


