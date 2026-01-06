# 🌐 Configuration Domaine OVH → Vercel + Render

## Objectif
Configurer `flowto.fr` (déjà acheté sur OVH) pour pointer vers :
- **flowto.fr** → Frontend Vercel
- **www.flowto.fr** → Frontend Vercel
- **api.flowto.fr** → Backend Render

---

## 📝 Étapes

### 1️⃣ Configurer DNS chez OVH (10 min)

#### A. Se connecter à OVH

1. **Va sur** : https://www.ovh.com/manager/
2. **Connecte-toi** avec ton compte
3. **Va dans** : `Web Cloud` → `Noms de domaine`
4. **Clique sur** : `flowto.fr`
5. **Va dans** : `Zone DNS`

---

#### B. Ajouter les Enregistrements DNS

**⚠️ IMPORTANT** : Avant de modifier, note les enregistrements existants !

##### 🎨 Frontend : flowto.fr → Vercel

**1. Enregistrement A pour le domaine racine**

```
Type : A
Sous-domaine : @ (ou vide)
Cible : 76.76.21.21
TTL : 300 (ou Auto)
```

**Pourquoi 76.76.21.21 ?** C'est l'IP de Vercel pour les domaines personnalisés.

**2. Enregistrement CNAME pour www**

```
Type : CNAME
Sous-domaine : www
Cible : cname.vercel-dns.com
TTL : 300 (ou Auto)
```

##### ⚙️ Backend : api.flowto.fr → Render

**3. Enregistrement CNAME pour api**

```
Type : CNAME
Sous-domaine : api
Cible : flowto-backend.onrender.com
TTL : 300 (ou Auto)
```

⚠️ **Remplace** `flowto-backend` par le vrai nom de ton service Render !

---

#### C. Sauvegarder les Modifications

1. **Vérifie** que tu as bien :
   - ✅ A record : `@` → `76.76.21.21`
   - ✅ CNAME : `www` → `cname.vercel-dns.com`
   - ✅ CNAME : `api` → `flowto-backend.onrender.com`

2. **Clique sur** : `Appliquer la configuration`

⏳ **Attends 5-30 minutes** pour la propagation DNS

---

### 2️⃣ Configurer le Domaine dans Vercel (5 min)

#### A. Ajouter flowto.fr

1. **Va sur** : https://vercel.com/dashboard
2. **Sélectionne** : `flowto-frontend` project
3. **Va dans** : `Settings` → `Domains`
4. **Clique sur** : `Add`
5. **Entre** : `flowto.fr`
6. **Clique sur** : `Add`

**Vercel te demande de configurer DNS** → Déjà fait chez OVH ✅

#### B. Ajouter www.flowto.fr

1. **Clique encore sur** : `Add`
2. **Entre** : `www.flowto.fr`
3. **Clique sur** : `Add`

#### C. Configuration de Redirection

**Vercel propose** :
```
Redirect www.flowto.fr → flowto.fr ?
```

**✅ Recommandé** : Oui (tous les utilisateurs vont sur la même URL)

---

### 3️⃣ Configurer le Domaine dans Render (5 min)

1. **Va sur** : https://dashboard.render.com
2. **Sélectionne** : `flowto-backend` service
3. **Va dans** : `Settings` → `Custom Domain`
4. **Clique sur** : `Add Custom Domain`
5. **Entre** : `api.flowto.fr`
6. **Clique sur** : `Save`

**Render vérifie le DNS** :
- ✅ Si DNS OK → Certificat SSL automatique en 1-2 min
- ⏳ Si pas encore propagé → Attends 10-30 min

---

### 4️⃣ Mettre à Jour les Variables d'Environnement (10 min)

**⚠️ IMPORTANT** : Maintenant que les domaines sont configurés, il faut mettre à jour les URLs !

#### A. Backend (Render)

**Va dans** : `flowto-backend` → `Environment`

**Modifie** : `CORS_ORIGINS`
```
CORS_ORIGINS=https://flowto.fr,https://www.flowto.fr,https://api.flowto.fr,https://flowto-frontend.vercel.app
```

**Clique sur** : `Save Changes`

**Le service redémarre automatiquement** (1-2 min)

---

#### B. Frontend (Vercel)

**Va dans** : `flowto-frontend` → `Settings` → `Environment Variables`

**Modifie** : `NEXT_PUBLIC_API_URL`
```
Name : NEXT_PUBLIC_API_URL
Value : https://api.flowto.fr
```

**Clique sur** : `Save`

**Puis** : `Deployments` → `...` → `Redeploy`

⏳ **Attends 1-2 minutes** (redeploy)

---

### 5️⃣ Vérifier que Tout Fonctionne (5 min)

#### ✅ Test 1 : Frontend
```
https://flowto.fr
```
**Tu devrais voir** : Homepage de Flowto

#### ✅ Test 2 : Redirection www
```
https://www.flowto.fr
```
**Tu devrais être redirigé vers** : `https://flowto.fr`

#### ✅ Test 3 : Backend
```
https://api.flowto.fr
```
**Tu devrais voir** :
```json
{
  "message": "Flowto API is running",
  "version": "1.0.0"
}
```

#### ✅ Test 4 : API Docs
```
https://api.flowto.fr/docs
```
**Tu devrais voir** : Interface Swagger

#### ✅ Test 5 : Connexion Frontend ↔ Backend

1. **Va sur** : https://flowto.fr/auth/register
2. **Crée un compte** test
3. **Login**
4. **Va sur** : Dashboard

**Si tout fonctionne** → Flowto est 100% opérationnel ! 🎉

---

## 📋 Récapitulatif DNS

| Sous-domaine | Type  | Cible                         | Usage                 |
|--------------|-------|-------------------------------|-----------------------|
| @            | A     | 76.76.21.21                   | Frontend (root)       |
| www          | CNAME | cname.vercel-dns.com          | Frontend (www)        |
| api          | CNAME | flowto-backend.onrender.com   | Backend (API)         |

---

## 🔒 SSL / HTTPS

- ✅ **Vercel** : SSL automatique (Let's Encrypt)
- ✅ **Render** : SSL automatique (Let's Encrypt)
- ✅ **Tout le trafic** : HTTPS uniquement

**Pas de config manuelle nécessaire !**

---

## ⏱️ Temps de Propagation DNS

- **Minimum** : 5 minutes
- **Moyenne** : 30 minutes
- **Maximum** : 24-48 heures (rare)

**Comment vérifier ?**

**Windows (PowerShell)** :
```powershell
nslookup flowto.fr
nslookup www.flowto.fr
nslookup api.flowto.fr
```

**Tu devrais voir** :
- `flowto.fr` → `76.76.21.21`
- `www.flowto.fr` → `cname.vercel-dns.com`
- `api.flowto.fr` → `flowto-backend.onrender.com`

---

## ✅ Checklist

- [ ] DNS configurés chez OVH
- [ ] A record : @ → 76.76.21.21
- [ ] CNAME : www → cname.vercel-dns.com
- [ ] CNAME : api → flowto-backend.onrender.com
- [ ] Domaines ajoutés dans Vercel (flowto.fr + www)
- [ ] Domaine ajouté dans Render (api.flowto.fr)
- [ ] CORS_ORIGINS mis à jour (Render)
- [ ] NEXT_PUBLIC_API_URL mis à jour (Vercel)
- [ ] Services redéployés
- [ ] flowto.fr accessible
- [ ] www.flowto.fr redirige vers flowto.fr
- [ ] api.flowto.fr accessible
- [ ] SSL actif partout (🔒 dans le navigateur)
- [ ] Frontend ↔ Backend connectés

---

## 🎯 URLs Finales

```
✅ Frontend     : https://flowto.fr
✅ Frontend www : https://www.flowto.fr (→ flowto.fr)
✅ Backend      : https://api.flowto.fr
✅ API Docs     : https://api.flowto.fr/docs
```

---

## 🆘 Problèmes Courants

### ❌ DNS ne propage pas après 1h

**Solution** :
1. Vérifie chez OVH que les enregistrements sont bien sauvegardés
2. Flush ton cache DNS local :
   ```powershell
   ipconfig /flushdns
   ```
3. Teste avec un outil en ligne : https://dnschecker.org

### ❌ SSL ne s'active pas

**Solution** :
- Attends 5-10 minutes après la propagation DNS
- Vercel/Render génèrent le certificat automatiquement
- Si bloqué > 30 min, contacte le support

### ❌ "ERR_SSL_VERSION_OR_CIPHER_MISMATCH"

**Solution** :
- Le DNS n'est pas encore propagé
- Attends encore 10-30 minutes

### ❌ Frontend fonctionne, mais API calls échouent

**Solution** :
1. Vérifie CORS_ORIGINS dans Render :
   ```
   CORS_ORIGINS=https://flowto.fr,https://www.flowto.fr,https://api.flowto.fr
   ```
2. Vérifie NEXT_PUBLIC_API_URL dans Vercel :
   ```
   NEXT_PUBLIC_API_URL=https://api.flowto.fr
   ```
3. Redéploie les deux services

### ❌ "This site can't be reached"

**Solution** :
- DNS pas encore propagé
- Attends encore
- Vérifie avec `nslookup flowto.fr`

---

## 🎉 Félicitations !

**Si tous les tests passent** → Flowto est officiellement en production ! 🚀

**Tu as maintenant** :
- ✅ Code sur GitHub
- ✅ Database PostgreSQL (Neon)
- ✅ Backend déployé (Render)
- ✅ Frontend déployé (Vercel)
- ✅ Domaine personnalisé (OVH)
- ✅ SSL/HTTPS partout
- ✅ Application accessible au monde entier !

---

**Créé le** : 6 janvier 2025  
**Projet** : Flowto - Automatisation Comptable PME  
**Domaine** : flowto.fr  
**Infrastructure** : Neon + Render + Vercel + OVH

