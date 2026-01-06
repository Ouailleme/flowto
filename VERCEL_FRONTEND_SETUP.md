# 🎨 Setup Frontend Vercel pour Flowto

## Pourquoi Vercel ?
- ✅ **Gratuit** : 100 GB bandwidth/mois
- ✅ **Créateurs de Next.js** : Optimisé pour Next.js
- ✅ **CDN Global** : Ultra rapide partout dans le monde
- ✅ **Deploy automatique** : Push sur GitHub = deploy auto
- ✅ **Preview** : URL unique pour chaque branche
- ✅ **HTTPS** : SSL automatique

---

## 📝 Étapes

### 1️⃣ Créer un Compte Vercel (1 min)

1. **Va sur** : https://vercel.com
2. **Clique sur** : `Sign Up`
3. **Choisis** : `Continue with GitHub` (le plus simple)
4. **Autorise** Vercel à accéder à ton compte GitHub

✅ **Tu es maintenant connecté à Vercel !**

---

### 2️⃣ Importer le Projet (2 min)

1. **Clique sur** : `Add New` → `Project`
2. **Vercel scanne tes repos GitHub**, tu devrais voir `flowto`
3. **Clique sur** : `Import` à côté de `flowto`

---

### 3️⃣ Configurer le Projet (3 min)

**Framework Preset** : Vercel détecte automatiquement Next.js ✅

**Configuration** :

```
Project Name: flowto-frontend
Framework Preset: Next.js (auto-détecté)
Root Directory: frontend
Build Command: npm run build (auto)
Output Directory: .next (auto)
Install Command: npm install (auto)
Node.js Version: 20.x (défaut)
```

**⚠️ IMPORTANT** : Clique sur `Root Directory` et sélectionne `frontend`

---

### 4️⃣ Ajouter les Variables d'Environnement (2 min)

**Avant de déployer**, il faut configurer les variables !

1. **Clique sur** : `Environment Variables`
2. **Ajoute ces variables** :

#### 🔌 Backend URL (IMPORTANT !)
```
Name: NEXT_PUBLIC_API_URL
Value: https://flowto-backend.onrender.com
```
⚠️ **Remplace** par l'URL de ton backend Render !

#### 🌐 Application
```
Name: NEXT_PUBLIC_APP_NAME
Value: Flowto

Name: NEXT_PUBLIC_DOMAIN
Value: flowto.fr

Name: NEXT_PUBLIC_ENVIRONMENT
Value: production

Name: NEXT_PUBLIC_VERSION
Value: 1.0.0
```

#### 📊 Monitoring (Optionnel - on configurera après)
```
Name: NEXT_PUBLIC_SENTRY_DSN
Value: (laisser vide pour l'instant)

Name: NEXT_PUBLIC_SENTRY_ENVIRONMENT
Value: production
```

3. **Vérifie** que toutes les variables sont bien ajoutées
4. **Clique sur** : `Deploy`

⏳ **Attends 1-2 minutes** (build du frontend)

---

### 5️⃣ Vérifier le Déploiement (1 min)

**Après le build** :

1. **Tu vois** : 🎉 Congratulations!
2. **Clique sur** : `Visit` ou copie l'URL
   ```
   https://flowto-frontend.vercel.app
   ```

3. **Ouvre** l'URL dans ton navigateur

✅ **Tu devrais voir** : La homepage de Flowto avec le design moderne !

---

## 🧪 Tests Rapides

### Test 1 : Homepage
```
https://flowto-frontend.vercel.app
```
**Tu devrais voir** :
- Logo Flowto
- "Automatisation comptable pour PME"
- Boutons "Se connecter" / "Créer un compte"

### Test 2 : Login
```
https://flowto-frontend.vercel.app/auth/login
```
**Tu devrais voir** : Page de connexion

### Test 3 : Register
```
https://flowto-frontend.vercel.app/auth/register
```
**Tu devrais voir** : Page d'inscription

### Test 4 : API Connection

1. **Crée un compte** sur `https://flowto-frontend.vercel.app/auth/register`
2. **Login**
3. **Va sur** : Dashboard
4. **Si tu vois** le dashboard → API connectée ✅

---

## 📋 Informations Importantes

### 🔗 URLs

**Production** : `https://flowto-frontend.vercel.app`  
**Dashboard** : https://vercel.com/dashboard

### 🚀 Deploys Automatiques

**Chaque push sur GitHub** = deploy automatique !

- **Branch `main`** → Production URL
- **Autres branches** → Preview URL unique

### 📊 Plan Gratuit - Limites

- **Bandwidth** : 100 GB/mois
- **Build Time** : 6000 minutes/mois
- **Invocations** : 100 GB-hours
- **Serverless Functions** : 100 heures

*(Largement suffisant pour commencer !)*

---

## 🌐 Configurer le Domaine Personnalisé (flowto.fr)

**On fera ça dans l'étape suivante** avec OVH !

---

## ✅ Checklist

- [ ] Compte Vercel créé
- [ ] Projet `flowto` importé
- [ ] Root Directory = `frontend`
- [ ] Variables d'environnement ajoutées
- [ ] NEXT_PUBLIC_API_URL configuré (backend Render)
- [ ] Build réussi
- [ ] URL Vercel copiée
- [ ] Homepage accessible
- [ ] Login/Register fonctionnent
- [ ] Connexion au backend OK

---

## 🎯 Prochaine Étape

**Frontend déployé ?** → On configure le domaine flowto.fr avec OVH ! 🌐

**URLs à garder** :
```
Frontend : https://flowto-frontend.vercel.app
Backend  : https://flowto-backend.onrender.com
```

---

## 🆘 Problèmes Courants

### ❌ Build échoue : "Module not found"

**Solution** :
- Vérifie que `Root Directory` = `frontend`
- Va dans Settings → Build & Development Settings
- Force un nouveau deploy

### ❌ Page blanche après deploy

**Solution** :
1. Ouvre la console navigateur (F12)
2. Cherche les erreurs
3. Souvent : `NEXT_PUBLIC_API_URL` mal configuré
4. Va dans Settings → Environment Variables
5. Vérifie que `NEXT_PUBLIC_API_URL` pointe vers Render

### ❌ "Failed to fetch" sur API calls

**Solution** :
1. Vérifie que le backend est bien démarré sur Render
2. Vérifie `CORS_ORIGINS` dans Render inclut Vercel URL
3. Exemple :
   ```
   CORS_ORIGINS=https://flowto-frontend.vercel.app,https://flowto.fr
   ```

### ❌ 404 sur les routes

**Solution** :
- Normal : Next.js utilise le routing dynamique
- Les routes sont gérées côté client
- Pas besoin de config supplémentaire

---

## 🔄 Redéployer

**Si tu changes les variables d'environnement** :

1. **Va dans** : Settings → Environment Variables
2. **Modifie** la variable
3. **Va dans** : Deployments
4. **Clique sur** : `...` → `Redeploy`

---

**Créé le** : 6 janvier 2025  
**Projet** : Flowto - Automatisation Comptable PME  
**Stack** : Next.js 15 + TypeScript + Vercel

