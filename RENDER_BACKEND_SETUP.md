# ⚙️ Setup Backend Render pour Flowto

## Pourquoi Render ?
- ✅ **Gratuit** : 750h/mois inclus (suffisant pour 1 service)
- ✅ **Simple** : Deploy automatique depuis GitHub
- ✅ **Europe** : Datacenter Frankfurt disponible
- ✅ **HTTPS** : SSL automatique
- ✅ **Logs** : Monitoring inclus

---

## 📝 Étapes

### 1️⃣ Créer un Compte Render (2 min)

1. **Va sur** : https://render.com
2. **Clique sur** : `Get Started`
3. **Choisis** : `Sign up with GitHub` (le plus simple)
4. **Autorise** Render à accéder à ton compte GitHub

✅ **Tu es maintenant connecté à Render !**

---

### 2️⃣ Connecter GitHub (1 min)

1. **Render te demande** : `Connect your GitHub account`
2. **Clique sur** : `Connect GitHub`
3. **Sélectionne** :
   - ⚫ Only select repositories
   - ✅ `flowto` (ton repository)
4. **Clique sur** : `Install`

✅ **Render a maintenant accès à ton repo Flowto !**

---

### 3️⃣ Créer le Web Service (3 min)

1. **Clique sur** : `New` → `Web Service`
2. **Sélectionne** : `flowto` (ton repository GitHub)
3. **Clique sur** : `Connect`

**Configuration** :

```
Name: flowto-backend
Region: Frankfurt (Europe) ⚠️ IMPORTANT pour RGPD
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type** :
```
⚫ Free (750h/mois - suffisant pour commencer)
```

**Clique sur** : `Create Web Service`

⏳ **Attends 2-3 minutes** (premier build)

---

### 4️⃣ Configurer les Variables d'Environnement (5 min)

**⚠️ IMPORTANT** : Le backend va crasher sans les variables d'environnement !

1. **Va dans** : `Environment` (menu de gauche)
2. **Clique sur** : `Add Environment Variable`

**Voici toutes les variables à ajouter** :

#### 🔧 Application
```
APP_NAME=Flowto API
APP_VERSION=1.0.0
DEBUG=false
```

#### 🗄️ Database (Neon)
```
DATABASE_URL=postgresql+asyncpg://[COPIE_TA_CONNECTION_STRING_NEON_ICI]
```
⚠️ **Remplace** `[COPIE_TA_CONNECTION_STRING_NEON_ICI]` par ta vraie connection string Neon !

**Exemple** :
```
DATABASE_URL=postgresql+asyncpg://flowto_user:AbCdEfGh123456@ep-cool-name-123456.eu-central-1.aws.neon.tech/flowto?sslmode=require
```

#### 🔐 Security
```
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
ALGORITHM=HS256
```

⚠️ **Générer un vrai SECRET_KEY** :
- **Windows** : Ouvre PowerShell
  ```powershell
  -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
  ```
- **Linux/Mac** :
  ```bash
  openssl rand -hex 32
  ```

#### 🌐 CORS
```
CORS_ORIGINS=https://flowto-backend.onrender.com,https://flowto.vercel.app,https://flowto.fr,https://www.flowto.fr,https://api.flowto.fr
```

#### 📊 Logging
```
LOG_LEVEL=INFO
LOG_FORMAT=json
SENTRY_ENVIRONMENT=production
```

#### 🎛️ Feature Flags (pour commencer)
```
ENABLE_AI_CATEGORIZATION=false
ENABLE_AUTO_RECONCILIATION=false
ENABLE_EMAIL_REMINDERS=false
```

#### 🔌 Redis (Optionnel pour MVP)
```
REDIS_URL=redis://localhost:6379
```
*(On peut désactiver Redis pour le MVP)*

#### 🚀 APIs Externes (on configurera après)
```
BRIDGE_API_KEY=
ANTHROPIC_API_KEY=
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=noreply@flowto.fr
SENTRY_DSN=
```
*(Laisser vide pour l'instant)*

3. **Clique sur** : `Save Changes`

---

### 5️⃣ Déployer (2 min)

1. **Le service redémarre automatiquement** après l'ajout des variables
2. **Va dans** : `Logs` (menu de gauche)
3. **Attends** que tu vois :
   ```
   ==> Starting service with 'uvicorn app.main:app --host 0.0.0.0 --port 10000'
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:10000
   ```

✅ **Si tu vois ça → Backend déployé avec succès ! 🎉**

---

### 6️⃣ Tester le Backend (1 min)

1. **Copie l'URL** en haut de la page :
   ```
   https://flowto-backend.onrender.com
   ```

2. **Ouvre dans ton navigateur** :
   ```
   https://flowto-backend.onrender.com/docs
   ```

3. **Tu devrais voir** : L'interface Swagger (documentation API interactive)

✅ **Si tu vois Swagger → Backend fonctionne parfaitement ! ✅**

---

## 🧪 Tests Rapides

### Test 1 : Health Check
```
https://flowto-backend.onrender.com/
```
**Réponse attendue** :
```json
{
  "message": "Flowto API is running",
  "version": "1.0.0"
}
```

### Test 2 : Swagger Documentation
```
https://flowto-backend.onrender.com/docs
```
**Tu devrais voir** : Interface Swagger complète avec tous les endpoints

---

## 📋 Informations Importantes

### 🔗 URLs Importantes

**Backend** : `https://flowto-backend.onrender.com`  
**API Docs** : `https://flowto-backend.onrender.com/docs`  
**Redoc** : `https://flowto-backend.onrender.com/redoc`

### 📊 Plan Gratuit - Limites

- **Compute** : 750h/mois (suffisant pour 1 service 24/7)
- **RAM** : 512 MB
- **Disk** : Éphémère (redémarre toutes les 15 min d'inactivité)
- **⚠️ Cold Start** : 30-50 secondes après 15 min d'inactivité

### 🔒 Sécurité

- ✅ HTTPS automatique (Let's Encrypt)
- ✅ Variables d'environnement sécurisées
- ✅ Logs centralisés

---

## ✅ Checklist

- [ ] Compte Render créé
- [ ] Repository GitHub connecté
- [ ] Web Service `flowto-backend` créé
- [ ] Region : Frankfurt (Europe)
- [ ] Variables d'environnement configurées
- [ ] SECRET_KEY généré (32+ caractères)
- [ ] DATABASE_URL (Neon) ajouté
- [ ] CORS_ORIGINS configuré
- [ ] Service démarré (logs OK)
- [ ] URL backend copiée
- [ ] Swagger accessible (`/docs`)

---

## 🎯 Prochaine Étape

**Backend déployé ?** → On configure le frontend sur Vercel ! 🚀

**URL à garder** :
```
https://flowto-backend.onrender.com
```
*(Tu en auras besoin pour configurer Vercel)*

---

## 🆘 Problèmes Courants

### ❌ Build échoue : "ModuleNotFoundError"

**Solution** :
- Vérifie que `Root Directory` = `backend`
- Vérifie que `requirements.txt` est présent

### ❌ Service crash au démarrage

**Solution** :
- Va dans `Logs`
- Cherche l'erreur (souvent DATABASE_URL manquant)
- Vérifie toutes les variables d'environnement

### ❌ "502 Bad Gateway"

**Solution** :
- Attends 1-2 minutes (premier démarrage)
- Vérifie les logs
- Redémarre le service si nécessaire

### ❌ Cold Start (lent après inactivité)

**Solution** :
- Normal sur le plan gratuit (15 min d'inactivité)
- Upgrade vers plan Starter (7$/mois) si nécessaire
- Ou configure un ping automatique toutes les 10 min

---

**Créé le** : 6 janvier 2025  
**Projet** : Flowto - Automatisation Comptable PME  
**Stack** : FastAPI + PostgreSQL + Render

