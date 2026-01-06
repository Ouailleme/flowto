# ✅ Checklist Complète Déploiement Flowto

## 📅 Plan de Déploiement

**Durée totale estimée** : 1h30  
**Coût** : ~10-15€/an (domaine + optionnel APIs)

---

## 🎯 Phase 1 : GitHub (5 min) - ✅ PRÊT

### Statut : 🟢 Code committé localement

**Fichiers créés** :
- ✅ `.gitignore`
- ✅ `GITHUB_SETUP.md` (guide détaillé)

**À faire** :
1. [ ] Créer repo GitHub : https://github.com/new
   - Name: `flowto`
   - Visibility: Private
   - ❌ Ne pas initialiser avec README
2. [ ] Exécuter ces commandes :
   ```bash
   git remote add origin https://github.com/[TON-USERNAME]/flowto.git
   git branch -M main
   git push -u origin main
   ```
3. [ ] Vérifier sur GitHub que tout est poussé

**Résultat attendu** :
```
✅ URL : https://github.com/[TON-USERNAME]/flowto
```

---

## 🗄️ Phase 2 : Database Neon (5 min)

### Statut : ⏳ À faire

**Fichier guide** : `NEON_DATABASE_SETUP.md`

**À faire** :
1. [ ] Créer compte : https://neon.tech
2. [ ] Créer projet `flowto`
3. [ ] Region : Frankfurt ou Amsterdam
4. [ ] Copier Connection String
5. [ ] Modifier en `postgresql+asyncpg://...`

**Résultat attendu** :
```
✅ Connection String : postgresql+asyncpg://user:pass@host/flowto?sslmode=require
```

---

## ⚙️ Phase 3 : Backend Render (15 min)

### Statut : ⏳ À faire

**Fichier guide** : `RENDER_BACKEND_SETUP.md`

**À faire** :
1. [ ] Créer compte : https://render.com
2. [ ] Connecter GitHub
3. [ ] Créer Web Service
   - Name: `flowto-backend`
   - Region: Frankfurt
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. [ ] Configurer variables d'environnement (voir guide)
5. [ ] Vérifier déploiement

**Variables critiques** :
- ✅ `DATABASE_URL` (depuis Neon)
- ✅ `SECRET_KEY` (générer avec `openssl rand -hex 32`)
- ✅ `CORS_ORIGINS`

**Résultat attendu** :
```
✅ Backend URL : https://flowto-backend.onrender.com
✅ Swagger     : https://flowto-backend.onrender.com/docs
```

---

## 🎨 Phase 4 : Frontend Vercel (15 min)

### Statut : ⏳ À faire

**Fichier guide** : `VERCEL_FRONTEND_SETUP.md`

**À faire** :
1. [ ] Créer compte : https://vercel.com
2. [ ] Importer projet GitHub
3. [ ] Configuration :
   - Name: `flowto-frontend`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
4. [ ] Configurer variables d'environnement
   - `NEXT_PUBLIC_API_URL` = URL backend Render
5. [ ] Déployer
6. [ ] Tester homepage + login

**Résultat attendu** :
```
✅ Frontend URL : https://flowto-frontend.vercel.app
```

---

## 🌐 Phase 5 : Domaine OVH → Vercel/Render (30 min)

### Statut : ⏳ À faire

**Fichier guide** : `OVH_DOMAIN_SETUP.md`

**À faire** :
1. [ ] Configurer DNS chez OVH :
   - A record: `@` → `76.76.21.21`
   - CNAME: `www` → `cname.vercel-dns.com`
   - CNAME: `api` → `flowto-backend.onrender.com`
2. [ ] Ajouter domaine dans Vercel :
   - `flowto.fr`
   - `www.flowto.fr`
3. [ ] Ajouter domaine dans Render :
   - `api.flowto.fr`
4. [ ] Mettre à jour variables d'environnement :
   - Render : `CORS_ORIGINS`
   - Vercel : `NEXT_PUBLIC_API_URL=https://api.flowto.fr`
5. [ ] Attendre propagation DNS (5-30 min)
6. [ ] Tester tous les domaines

**Résultat attendu** :
```
✅ https://flowto.fr          (frontend)
✅ https://www.flowto.fr      (→ flowto.fr)
✅ https://api.flowto.fr      (backend)
✅ https://api.flowto.fr/docs (swagger)
```

---

## 🔌 Phase 6 : APIs Externes (Optionnel - 30 min)

### Statut : ⏳ À faire plus tard

**Fichier guide** : `SETUP_APIS_GUIDE.md`

Ces APIs ne sont pas critiques pour le MVP :

### A. Sentry (Monitoring - Gratuit)
- [ ] Créer compte : https://sentry.io
- [ ] Créer projet Backend (Python)
- [ ] Créer projet Frontend (Next.js)
- [ ] Copier DSN
- [ ] Ajouter dans variables d'environnement

### B. SendGrid (Emails - Gratuit 100/jour)
- [ ] Créer compte : https://sendgrid.com
- [ ] Créer API Key
- [ ] Vérifier domaine (SPF/DKIM)
- [ ] Ajouter `SENDGRID_API_KEY`

### C. Bridge API (Agrégation bancaire - Gratuit test)
- [ ] Créer compte : https://dashboard.bridgeapi.io
- [ ] Obtenir clés API test
- [ ] Ajouter `BRIDGE_API_KEY`

### D. Anthropic (IA - ~5€/mois)
- [ ] Créer compte : https://console.anthropic.com
- [ ] Obtenir API key
- [ ] Ajouter 10€ de crédit
- [ ] Ajouter `ANTHROPIC_API_KEY`

**Feature flags** : Laisser à `false` jusqu'à configuration complète

---

## 🧪 Phase 7 : Tests de Production (15 min)

### Statut : ⏳ À faire après déploiement

**À tester** :

### Frontend
- [ ] Homepage accessible
- [ ] Design responsive (mobile/desktop)
- [ ] Navigation fluide

### Authentication
- [ ] Création de compte
- [ ] Login
- [ ] Logout
- [ ] Tokens refresh

### Features
- [ ] Dashboard affiche les stats
- [ ] Créer une facture
- [ ] Liste des factures
- [ ] Modifier une facture
- [ ] Supprimer une facture
- [ ] Ajouter une transaction
- [ ] Filtrer les transactions

### Performance
- [ ] Temps de chargement < 3s
- [ ] API response time < 500ms
- [ ] Pas d'erreurs console

### Sécurité
- [ ] HTTPS partout (🔒)
- [ ] Headers sécurisés
- [ ] CORS fonctionne
- [ ] Tokens JWT valides

---

## 📊 Récapitulatif Technique

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     UTILISATEUR                          │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   flowto.fr (OVH)     │
            │   DNS Configuration    │
            └───────────┬───────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌───────────────┐               ┌───────────────┐
│   Vercel      │               │   Render      │
│   Frontend    │◄─────────────►│   Backend     │
│   Next.js     │   API Calls   │   FastAPI     │
└───────────────┘               └───────┬───────┘
                                        │
                                        ▼
                                ┌───────────────┐
                                │   Neon.tech   │
                                │   PostgreSQL  │
                                └───────────────┘
```

### Stack Technique

| Composant | Technologie | Hébergement | Coût |
|-----------|-------------|-------------|------|
| **Frontend** | Next.js 15 + TypeScript | Vercel | Gratuit |
| **Backend** | FastAPI + Python 3.12 | Render | Gratuit |
| **Database** | PostgreSQL 16 | Neon.tech | Gratuit |
| **Domaine** | flowto.fr | OVH | ~10€/an |
| **SSL** | Let's Encrypt | Auto | Gratuit |
| **Monitoring** | Sentry | Sentry.io | Gratuit |

**Total** : ~10€/an + optionnel APIs (~5€/mois)

---

## ✅ Checklist Finale

### Pré-déploiement
- [x] Code committé localement
- [x] .gitignore créé
- [x] Guides créés
- [ ] Code sur GitHub

### Infrastructure
- [ ] Database Neon créée
- [ ] Backend Render déployé
- [ ] Frontend Vercel déployé

### Domaine
- [ ] DNS configurés chez OVH
- [ ] Domaines liés (Vercel + Render)
- [ ] SSL actif partout

### Tests
- [ ] Application accessible
- [ ] Toutes les features fonctionnent
- [ ] Performance OK
- [ ] Sécurité OK

### Optionnel
- [ ] Monitoring Sentry configuré
- [ ] Emails SendGrid configurés
- [ ] APIs externes configurées

---

## 🎯 URLs de Référence

### Guides Détaillés
- `GITHUB_SETUP.md` - GitHub
- `NEON_DATABASE_SETUP.md` - Database
- `RENDER_BACKEND_SETUP.md` - Backend
- `VERCEL_FRONTEND_SETUP.md` - Frontend
- `OVH_DOMAIN_SETUP.md` - Domaine
- `SETUP_APIS_GUIDE.md` - APIs externes
- `DEPLOY_INSTRUCTIONS.md` - Guide complet

### Services
- **GitHub** : https://github.com
- **Neon** : https://neon.tech
- **Render** : https://render.com
- **Vercel** : https://vercel.com
- **OVH** : https://www.ovh.com/manager/
- **Sentry** : https://sentry.io
- **SendGrid** : https://sendgrid.com
- **Bridge** : https://bridgeapi.io
- **Anthropic** : https://console.anthropic.com

---

## 🆘 Support

### En cas de problème

1. **Consulte le guide spécifique** à l'étape bloquée
2. **Vérifie les logs** :
   - Backend : Render Dashboard → Logs
   - Frontend : Vercel Dashboard → Logs
3. **Teste les connexions** :
   - DNS : `nslookup flowto.fr`
   - API : `curl https://api.flowto.fr`
4. **Variables d'environnement** : Souvent la cause des problèmes !

### Commandes Utiles

```powershell
# Tester DNS
nslookup flowto.fr
nslookup api.flowto.fr

# Flush DNS local
ipconfig /flushdns

# Tester API
curl https://api.flowto.fr
curl https://api.flowto.fr/docs

# Git status
git status
git log --oneline -5
```

---

## 🎉 Félicitations !

**Une fois toutes les cases cochées** → Flowto est en production ! 🚀

**Tu auras alors** :
- ✅ Application accessible au monde entier
- ✅ Infrastructure scalable
- ✅ Domaine personnalisé
- ✅ SSL/HTTPS sécurisé
- ✅ CI/CD automatisé (GitHub Actions)
- ✅ Monitoring en place

**Prochaines étapes** :
- 📊 Analyser les premiers utilisateurs
- 🚀 Ajouter les APIs externes
- 📈 Optimiser les performances
- 💡 Développer nouvelles features

---

**Créé le** : 6 janvier 2025  
**Projet** : Flowto - Automatisation Comptable PME  
**Version** : 1.0.0  
**Status** : 🟢 Ready to deploy

