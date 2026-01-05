# 🚀 Plan de Déploiement - Flowto

**Objectif** : Mettre Flowto en production sur **flowto.fr**

---

## 📋 Checklist Complète

### Phase 1 : Domaine & DNS (15 min)
- [ ] Acheter le domaine **flowto.fr** (OVH, Gandi, Namecheap)
- [ ] Configurer les DNS
  - [ ] A record : `flowto.fr` → IP du serveur
  - [ ] CNAME : `www.flowto.fr` → `flowto.fr`
  - [ ] CNAME : `api.flowto.fr` → backend
  - [ ] MX records : pour les emails

### Phase 2 : Déploiement Backend (30 min)
- [ ] Choisir hébergeur backend
  - Option 1 : **Render** (recommandé, gratuit pour commencer)
  - Option 2 : Railway
  - Option 3 : Fly.io
  - Option 4 : VPS (DigitalOcean, Scaleway)

- [ ] Créer base de données PostgreSQL
  - Option 1 : **Neon** (gratuit, serverless)
  - Option 2 : Supabase
  - Option 3 : Render PostgreSQL
  - Option 4 : Database hébergeur

- [ ] Configurer variables d'environnement
- [ ] Déployer backend
- [ ] Vérifier health check

### Phase 3 : Déploiement Frontend (20 min)
- [ ] Choisir hébergeur frontend
  - Option 1 : **Vercel** (recommandé, Next.js natif)
  - Option 2 : Netlify
  - Option 3 : Cloudflare Pages

- [ ] Connecter le repo GitHub
- [ ] Configurer variables d'environnement
- [ ] Déployer frontend
- [ ] Configurer domaine custom

### Phase 4 : APIs Externes (45 min)
- [ ] **Bridge API** (Agrégation bancaire)
  - [ ] Créer compte sur bridgeapi.io
  - [ ] Obtenir API key
  - [ ] Configurer webhook
  - [ ] Tester connexion

- [ ] **Anthropic Claude** (IA)
  - [ ] Créer compte Anthropic
  - [ ] Obtenir API key
  - [ ] Configurer limites
  - [ ] Tester catégorisation

- [ ] **SendGrid** (Emails)
  - [ ] Créer compte SendGrid
  - [ ] Vérifier domaine (SPF, DKIM)
  - [ ] Obtenir API key
  - [ ] Créer templates emails

### Phase 5 : Monitoring (30 min)
- [ ] **Sentry** (Error tracking)
  - [ ] Créer compte Sentry
  - [ ] Créer projet backend
  - [ ] Créer projet frontend
  - [ ] Obtenir DSN
  - [ ] Tester error tracking

- [ ] **Uptime Monitoring** (optionnel)
  - Option 1 : UptimeRobot (gratuit)
  - Option 2 : Better Uptime
  - Option 3 : Pingdom

### Phase 6 : Sécurité & SSL (15 min)
- [ ] Vérifier SSL/TLS (auto avec Vercel/Render)
- [ ] Configurer CORS production
- [ ] Configurer rate limiting
- [ ] Tester authentification
- [ ] Configurer backup DB (optionnel)

### Phase 7 : Tests Production (20 min)
- [ ] Créer compte test
- [ ] Tester authentification
- [ ] Tester création facture
- [ ] Tester connexion bancaire (si API configurée)
- [ ] Vérifier emails
- [ ] Vérifier logs Sentry

---

## 🎯 Configuration Recommandée (Gratuite pour Démarrer)

### Backend : Render (Free Tier)
**Avantages** :
- Gratuit jusqu'à 750h/mois
- Deploy automatique depuis GitHub
- PostgreSQL inclus
- SSL automatique
- Simple à configurer

**Configuration** :
```bash
Service: Web Service
Repository: votre-repo/flowto
Branch: main
Build Command: pip install -r backend/requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Root Directory: backend
```

### Frontend : Vercel (Free Tier)
**Avantages** :
- Gratuit (bande passante illimitée)
- Next.js optimisé nativement
- Deploy automatique depuis GitHub
- DNS + SSL inclus
- CDN global

**Configuration** :
```bash
Framework: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### Database : Neon (Free Tier)
**Avantages** :
- PostgreSQL serverless
- 3 GB de stockage gratuit
- Pas de carte de crédit requise
- Backups automatiques
- Scaling automatique

### Redis : Upstash (Free Tier)
**Avantages** :
- Redis serverless
- 10,000 commandes/jour gratuit
- Pas de carte de crédit requise

---

## 📝 Variables d'Environnement Production

### Backend (Render)

```bash
# Application
APP_NAME=Flowto API
APP_VERSION=1.0.0
DEBUG=false

# Database (Neon)
DATABASE_URL=postgresql+asyncpg://[user]:[password]@[host]/[db]?sslmode=require

# Redis (Upstash)
REDIS_URL=rediss://default:[password]@[host]:6379

# Security
SECRET_KEY=[générer avec: openssl rand -hex 32]
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# CORS
CORS_ORIGINS=https://flowto.fr,https://www.flowto.fr

# Bridge API
BRIDGE_API_KEY=[votre_clé_bridge]
BRIDGE_API_URL=https://api.bridgeapi.io/v2

# Anthropic
ANTHROPIC_API_KEY=[votre_clé_anthropic]

# SendGrid
SENDGRID_API_KEY=[votre_clé_sendgrid]
SENDGRID_FROM_EMAIL=noreply@flowto.fr

# Sentry
SENTRY_DSN=[votre_dsn_sentry]
SENTRY_ENVIRONMENT=production

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Frontend (Vercel)

```bash
# API
NEXT_PUBLIC_API_URL=https://api.flowto.fr

# Sentry
NEXT_PUBLIC_SENTRY_DSN=[votre_dsn_sentry_frontend]
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_VERSION=1.0.0

# Domain
NEXT_PUBLIC_DOMAIN=flowto.fr
```

---

## 🔧 Guide Étape par Étape

### Étape 1 : Acheter le Domaine (5 min)

**OVH (recommandé pour .fr)** :
1. Aller sur ovh.com
2. Rechercher "flowto.fr"
3. Acheter (~10€/an)
4. Accéder au panneau de configuration

**Cloudflare (optionnel mais recommandé)** :
1. Créer compte Cloudflare
2. Ajouter le domaine flowto.fr
3. Configurer les nameservers chez OVH
4. Activer proxy + SSL

### Étape 2 : Déployer Backend sur Render (10 min)

1. **Créer compte Render** : https://render.com
2. **New Web Service** → Connect GitHub
3. **Configuration** :
   ```
   Name: flowto-backend
   Region: Frankfurt (Europe)
   Branch: main
   Root Directory: backend
   Runtime: Python 3.12
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```
4. **Ajouter variables d'environnement** (voir section ci-dessus)
5. **Deploy** → Attendre 2-3 min
6. **Tester** : `https://flowto-backend.onrender.com/health`

### Étape 3 : Créer Database Neon (5 min)

1. **Créer compte Neon** : https://neon.tech
2. **New Project** :
   ```
   Name: flowto
   Region: Europe
   PostgreSQL: 16
   ```
3. **Copier connection string** :
   ```
   postgresql+asyncpg://[user]:[password]@[host]/[db]?sslmode=require
   ```
4. **Ajouter dans Render** → Variables d'environnement → `DATABASE_URL`
5. **Redéployer backend**

### Étape 4 : Déployer Frontend sur Vercel (10 min)

1. **Créer compte Vercel** : https://vercel.com
2. **Import Project** → Connect GitHub
3. **Configuration** :
   ```
   Framework: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next (auto-détecté)
   Install Command: npm install
   ```
4. **Environment Variables** :
   ```
   NEXT_PUBLIC_API_URL=https://flowto-backend.onrender.com
   (ajouter les autres variables)
   ```
5. **Deploy** → Attendre 1-2 min
6. **Tester** : `https://flowto-frontend.vercel.app`

### Étape 5 : Configurer Domaines (10 min)

**Backend (Render)** :
1. Render Dashboard → Settings → Custom Domain
2. Ajouter : `api.flowto.fr`
3. Copier CNAME : `flowto-backend.onrender.com`
4. DNS (OVH/Cloudflare) :
   ```
   Type: CNAME
   Name: api
   Target: flowto-backend.onrender.com
   ```

**Frontend (Vercel)** :
1. Vercel Dashboard → Settings → Domains
2. Ajouter : `flowto.fr` et `www.flowto.fr`
3. DNS (OVH/Cloudflare) :
   ```
   Type: A
   Name: @
   Target: 76.76.21.21 (IP Vercel)
   
   Type: CNAME
   Name: www
   Target: cname.vercel-dns.com
   ```

### Étape 6 : Configurer APIs Externes

#### Bridge API (Agrégation Bancaire)

1. **Créer compte** : https://bridgeapi.io
2. **Dashboard** → API Keys → Create Key
3. **Copier API key**
4. **Ajouter dans Render** :
   ```
   BRIDGE_API_KEY=votre_clé
   ```
5. **Configurer Webhook** :
   ```
   URL: https://api.flowto.fr/webhooks/bridge
   Events: transaction.created, account.updated
   ```

#### Anthropic Claude (IA)

1. **Créer compte** : https://console.anthropic.com
2. **API Keys** → Create Key
3. **Copier API key**
4. **Ajouter dans Render** :
   ```
   ANTHROPIC_API_KEY=votre_clé
   ```
5. **Configurer limites** (optionnel)

#### SendGrid (Emails)

1. **Créer compte** : https://sendgrid.com (gratuit 100 emails/jour)
2. **Settings** → API Keys → Create Key
3. **Copier API key**
4. **Vérifier domaine** :
   - Settings → Sender Authentication
   - Authenticate Your Domain → flowto.fr
   - Copier records DNS (SPF, DKIM, DMARC)
   - Ajouter dans DNS
5. **Ajouter dans Render** :
   ```
   SENDGRID_API_KEY=votre_clé
   SENDGRID_FROM_EMAIL=noreply@flowto.fr
   ```

#### Sentry (Monitoring)

1. **Créer compte** : https://sentry.io
2. **Create Project** :
   - Platform: Python (backend)
   - Name: flowto-backend
3. **Copier DSN** :
   ```
   https://[key]@[org].ingest.sentry.io/[project]
   ```
4. **Répéter pour frontend** (Platform: Next.js)
5. **Ajouter dans Render + Vercel** :
   ```
   SENTRY_DSN=votre_dsn
   ```

---

## ✅ Checklist Post-Déploiement

- [ ] **URLs accessibles**
  - [ ] https://flowto.fr → Frontend OK
  - [ ] https://api.flowto.fr → Backend OK
  - [ ] https://api.flowto.fr/docs → Swagger OK

- [ ] **SSL/HTTPS**
  - [ ] Certificat valide
  - [ ] Pas d'erreurs mixed content

- [ ] **Tests Fonctionnels**
  - [ ] Inscription utilisateur
  - [ ] Login
  - [ ] Création facture
  - [ ] Email envoyé (SendGrid)
  - [ ] Logs dans Sentry

- [ ] **Performance**
  - [ ] Temps de chargement < 3s
  - [ ] API response < 500ms
  - [ ] Lighthouse score > 90

- [ ] **Monitoring**
  - [ ] Sentry erreurs trackées
  - [ ] Uptime monitoring actif
  - [ ] Logs consultables

---

## 💰 Coûts Estimés

### Configuration Gratuite (jusqu'à 100 utilisateurs)
```
Domaine (.fr)       : 10€/an
Render (backend)    : 0€ (free tier)
Vercel (frontend)   : 0€ (free tier)
Neon (database)     : 0€ (free tier)
Upstash (redis)     : 0€ (free tier)
Bridge API          : 0€ (dev account)
Anthropic           : ~5€/mois (usage)
SendGrid            : 0€ (100 emails/jour)
Sentry              : 0€ (5k events/mois)
─────────────────────────────────
TOTAL Premier mois  : ~15€
TOTAL Mensuel       : ~5-10€
```

### Configuration Production (1000+ utilisateurs)
```
Domaine             : 10€/an
Render Pro          : 25€/mois
Vercel Pro          : 20€/mois
Neon Scale          : 19€/mois
Upstash             : 10€/mois
Bridge API          : Sur devis
Anthropic           : ~50€/mois
SendGrid            : 15€/mois (40k emails)
Sentry Business     : 26€/mois
─────────────────────────────────
TOTAL Mensuel       : ~165€/mois
```

---

## 🎯 Timeline

**Jour 1 (2-3h)** :
- Acheter domaine
- Déployer backend + DB
- Déployer frontend
- Configurer DNS

**Jour 2 (2-3h)** :
- Configurer APIs externes
- Configurer monitoring
- Tests fonctionnels

**Jour 3 (1h)** :
- Tests utilisateurs
- Ajustements
- Documentation

**Total : 5-7h de setup** ⚡

---

## 📞 Support & Ressources

### Documentation
- Render : https://render.com/docs
- Vercel : https://vercel.com/docs
- Neon : https://neon.tech/docs
- Bridge : https://docs.bridgeapi.io
- Anthropic : https://docs.anthropic.com
- SendGrid : https://docs.sendgrid.com

### Communautés
- Discord Render
- Discord Vercel
- Stack Overflow

---

**Prêt à déployer Flowto en production ! 🚀**

