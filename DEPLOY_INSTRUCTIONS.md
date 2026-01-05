# 🚀 Instructions de Déploiement Flowto

## ✅ Statut Actuel
- [x] Compte GitHub créé
- [x] Domaine flowto.fr acheté (OVH)
- [ ] Code pushé sur GitHub
- [ ] Services déployés

---

## 📦 ÉTAPE 1 : Pusher le Code sur GitHub (5 min)

### A. Créer le Repository GitHub

1. **Va sur GitHub** : https://github.com/new
2. **Paramètres** :
   ```
   Repository name: flowto
   Description: Automatisation comptable pour PME - flowto.fr
   Visibility: Private (recommandé)
   ❌ Ne pas initialiser avec README, .gitignore, ou license (on les a déjà)
   ```
3. **Create repository**
4. **Copier l'URL** : `https://github.com/[ton-username]/flowto.git`

### B. Initialiser Git Local

**Ouvre PowerShell dans le dossier du projet** et exécute :

```powershell
# Initialiser Git (si pas déjà fait)
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Flowto v1.0"

# Lier au repo GitHub (remplace [ton-username])
git remote add origin https://github.com/[ton-username]/flowto.git

# Renommer la branche en main
git branch -M main

# Pusher le code
git push -u origin main
```

**Si tu as des erreurs d'authentification GitHub** :
```powershell
# Utiliser un Personal Access Token
# GitHub → Settings → Developer settings → Personal access tokens → Generate new token
# Scopes : repo (tous), workflow
# Utilise le token comme mot de passe
```

✅ **Vérifie** : Va sur GitHub, tu devrais voir tout ton code !

---

## 🗄️ ÉTAPE 2 : Database Neon (5 min)

### A. Créer Compte Neon

1. **Va sur** : https://neon.tech
2. **Sign up** (avec GitHub pour aller vite)
3. **Create a project** :
   ```
   Project name: flowto
   PostgreSQL: 16 (dernière version)
   Region: Europe (Frankfurt ou Amsterdam)
   ```

### B. Obtenir Connection String

1. **Dashboard** → **Connection Details**
2. **Copier** : `Connection string`
   ```
   Format: postgresql://[user]:[password]@[host]/[db]?sslmode=require
   ```
3. **Important** : Remplacer `postgresql://` par `postgresql+asyncpg://`
   ```
   postgresql+asyncpg://[user]:[password]@[host]/[db]?sslmode=require
   ```

✅ **Note cette connection string** pour l'étape suivante !

---

## ⚙️ ÉTAPE 3 : Backend Render (15 min)

### A. Créer Compte Render

1. **Va sur** : https://render.com
2. **Sign up** (avec GitHub pour connecter le repo)

### B. Créer Web Service

1. **New** → **Web Service**
2. **Connect GitHub** → Autoriser l'accès
3. **Sélectionner** : `flowto` repository
4. **Configuration** :
   ```
   Name: flowto-backend
   Region: Frankfurt (Europe)
   Branch: main
   Root Directory: backend
   Runtime: Python 3.12
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

### C. Variables d'Environnement

**Dans Render → Environment** :

```bash
# Application
APP_NAME=Flowto API
APP_VERSION=1.0.0
DEBUG=false

# Database (colle ta connection string Neon ici !)
DATABASE_URL=postgresql+asyncpg://[user]:[password]@[host]/[db]?sslmode=require

# Redis (Upstash - voir annexe)
REDIS_URL=redis://localhost:6379

# Security (générer avec: openssl rand -hex 32 dans WSL ou Git Bash)
SECRET_KEY=change-this-to-a-random-32-char-string
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
ALGORITHM=HS256

# CORS (on ajoutera flowto.fr après)
CORS_ORIGINS=https://flowto-backend.onrender.com,https://flowto.vercel.app

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
SENTRY_ENVIRONMENT=production

# Feature flags
ENABLE_AI_CATEGORIZATION=false
ENABLE_AUTO_RECONCILIATION=false
ENABLE_EMAIL_REMINDERS=false
```

### D. Déployer

1. **Create Web Service**
2. **Attendre 2-3 minutes** (build + deploy)
3. **Vérifier** : Clique sur l'URL générée → `https://flowto-backend.onrender.com`
4. **Tester** : Ajoute `/docs` → Tu devrais voir Swagger !

✅ **URL Backend** : https://flowto-backend.onrender.com

---

## 🎨 ÉTAPE 4 : Frontend Vercel (15 min)

### A. Créer Compte Vercel

1. **Va sur** : https://vercel.com
2. **Sign up** (avec GitHub)

### B. Importer Projet

1. **Add New** → **Project**
2. **Import Git Repository** → Sélectionner `flowto`
3. **Configuration** :
   ```
   Framework Preset: Next.js (auto-détecté)
   Root Directory: frontend
   Build Command: npm run build (auto)
   Output Directory: .next (auto)
   Install Command: npm install (auto)
   ```

### C. Variables d'Environnement

**Dans Vercel → Settings → Environment Variables** :

```bash
# API URL (URL de ton backend Render)
NEXT_PUBLIC_API_URL=https://flowto-backend.onrender.com

# Monitoring (optionnel pour l'instant)
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_VERSION=1.0.0
NEXT_PUBLIC_DOMAIN=flowto.fr
```

### D. Déployer

1. **Deploy**
2. **Attendre 1-2 minutes**
3. **Vérifier** : Clique sur l'URL → `https://flowto.vercel.app`

✅ **URL Frontend** : https://flowto.vercel.app

---

## 🌐 ÉTAPE 5 : Configurer Domaine OVH → Vercel/Render (30 min)

### A. Configurer DNS chez OVH

**Connecte-toi à OVH → DNS**

**Pour le Frontend (flowto.fr → Vercel)** :

1. **Ajouter un enregistrement A** :
   ```
   Type: A
   Sous-domaine: @ (ou vide)
   Cible: 76.76.21.21 (IP Vercel)
   TTL: 300
   ```

2. **Ajouter un enregistrement CNAME pour www** :
   ```
   Type: CNAME
   Sous-domaine: www
   Cible: cname.vercel-dns.com
   TTL: 300
   ```

**Pour le Backend (api.flowto.fr → Render)** :

3. **Ajouter un enregistrement CNAME** :
   ```
   Type: CNAME
   Sous-domaine: api
   Cible: flowto-backend.onrender.com
   TTL: 300
   ```

### B. Configurer Domaine dans Vercel

1. **Vercel Dashboard** → **Settings** → **Domains**
2. **Add** : `flowto.fr`
3. **Add** : `www.flowto.fr`
4. **Attendre validation** (5-10 min)

### C. Configurer Domaine dans Render

1. **Render Dashboard** → **Settings** → **Custom Domain**
2. **Add** : `api.flowto.fr`
3. **Attendre validation** (5-10 min)

### D. Mettre à jour les CORS

**Dans Render → Environment Variables** :

```bash
# Mettre à jour CORS_ORIGINS
CORS_ORIGINS=https://flowto.fr,https://www.flowto.fr,https://api.flowto.fr
```

**Dans Vercel → Environment Variables** :

```bash
# Mettre à jour API_URL
NEXT_PUBLIC_API_URL=https://api.flowto.fr
```

**Redéployer les deux services** après ces changements !

✅ **Flowto accessible sur** : https://flowto.fr 🎉

---

## 🎯 ÉTAPE 6 : Tests de Base (10 min)

1. **Va sur** : https://flowto.fr
2. **Créer un compte** : 
   - Email : test@flowto.fr
   - Password : Test123!
3. **Login**
4. **Créer une facture** test
5. **Vérifier** que tout fonctionne

✅ **Si tout marche** → Flowto est en production ! 🚀

---

## 📊 URLs Finales

```
✅ Frontend:     https://flowto.fr
✅ Backend:      https://api.flowto.fr  
✅ API Docs:     https://api.flowto.fr/docs
```

---

## 🔧 ANNEXES (Optionnel)

### Redis avec Upstash (Gratuit)

1. **Va sur** : https://upstash.com
2. **Create Database** :
   ```
   Name: flowto-cache
   Region: eu-west-1
   ```
3. **Copier** : `UPSTASH_REDIS_URL`
4. **Dans Render** : `REDIS_URL=[url_upstash]`

### Sentry (Monitoring - Gratuit)

1. **Va sur** : https://sentry.io
2. **Create Project** :
   - Platform: Python
   - Name: flowto-backend
3. **Copier DSN**
4. **Dans Render** : `SENTRY_DSN=[ton_dsn]`

---

## ✅ Checklist Finale

- [ ] Code sur GitHub
- [ ] Database Neon créée
- [ ] Backend sur Render
- [ ] Frontend sur Vercel
- [ ] DNS configurés (OVH)
- [ ] flowto.fr accessible
- [ ] api.flowto.fr accessible
- [ ] Compte test créé
- [ ] Application fonctionnelle

**Si tout est ✅ → BRAVO ! Flowto est en production ! 🎉**

---

## 🆘 Besoin d'Aide ?

- Backend ne démarre pas ? → Vérifie les logs dans Render
- Frontend erreur 500 ? → Vérifie NEXT_PUBLIC_API_URL
- DNS ne marche pas ? → Attends 30 min (propagation DNS)
- 401 sur API ? → Vérifie CORS_ORIGINS

**Garde ce document sous la main pendant le déploiement !**

