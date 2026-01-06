# 🚀 Setup GitHub pour Flowto

## ✅ Ce qui est déjà fait :
- [x] Code commité localement
- [x] .gitignore configuré
- [x] Fichiers .env.example créés

## 📝 À faire maintenant :

### 1️⃣ Créer le Repository GitHub (2 min)

**Va sur** : https://github.com/new

**Paramètres** :
```
Repository name: flowto
Description: Automatisation comptable PME - flowto.fr
Visibility: ⚫ Private (recommandé)

❌ Ne pas cocher :
   - Add a README file
   - Add .gitignore
   - Choose a license
```

**Clique sur** : `Create repository`

---

### 2️⃣ Obtenir l'URL du Repository

Après la création, GitHub affiche une page avec plusieurs commandes.

**Copie l'URL** qui ressemble à :
```
https://github.com/[TON-USERNAME]/flowto.git
```

**Exemple** :
```
https://github.com/johndoe/flowto.git
```

---

### 3️⃣ Lier le Repository Local à GitHub

**Ouvre PowerShell** dans `C:\Users\yvesm\Documents\Projet`

**Exécute ces commandes** (remplace `[TON-USERNAME]` par ton vrai username GitHub) :

```powershell
# 1. Lier le repository local à GitHub
git remote add origin https://github.com/[TON-USERNAME]/flowto.git

# 2. Renommer la branche en main (standard moderne)
git branch -M main

# 3. Pusher le code
git push -u origin main
```

---

### 4️⃣ Authentification GitHub

**Si GitHub demande ton mot de passe** :

GitHub a désactivé l'authentification par mot de passe. Tu dois créer un **Personal Access Token (PAT)**.

#### A. Créer un Token

1. **Va sur** : https://github.com/settings/tokens
2. **Clique sur** : `Generate new token` → `Tokens (classic)`
3. **Note** : `Flowto deployment token`
4. **Expiration** : 90 days (ou plus)
5. **Scopes** (cocher ces cases) :
   - ✅ **repo** (tous les sous-items)
   - ✅ **workflow**
6. **Generate token**
7. **⚠️ IMPORTANT** : Copie le token maintenant, tu ne pourras plus le voir !

#### B. Utiliser le Token

Quand `git push` demande un mot de passe :
- **Username** : Ton username GitHub
- **Password** : Colle le token (pas ton vrai mot de passe !)

---

### 5️⃣ Vérifier que ça a marché

1. **Va sur** : https://github.com/[TON-USERNAME]/flowto
2. **Tu devrais voir** :
   - Tous tes fichiers
   - Le commit "🚀 Initial commit - Flowto v1.0 - Production ready"
   - Les dossiers `backend/`, `frontend/`, etc.

✅ **Si tu vois tout ça → C'EST BON ! ✅**

---

## 🎯 Étapes Suivantes

Une fois le code sur GitHub, on va déployer :

1. ✅ **GitHub** → Fait !
2. 🗄️ **Database** (Neon.tech) → 5 min
3. ⚙️ **Backend** (Render) → 15 min
4. 🎨 **Frontend** (Vercel) → 15 min
5. 🌐 **Domaine** (OVH → Vercel/Render) → 30 min

**Total** : ~1h15 pour avoir Flowto en prod !

---

## 🆘 Problèmes Courants

### ❌ Erreur : "remote origin already exists"

**Solution** :
```powershell
git remote remove origin
git remote add origin https://github.com/[TON-USERNAME]/flowto.git
```

### ❌ Erreur : "authentication failed"

**Solution** : Utilise un Personal Access Token (voir section 4)

### ❌ Erreur : "failed to push some refs"

**Solution** :
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## ✅ Checklist

- [ ] Repository `flowto` créé sur GitHub
- [ ] URL du repository copiée
- [ ] `git remote add origin` exécuté
- [ ] `git branch -M main` exécuté
- [ ] `git push -u origin main` exécuté
- [ ] Code visible sur GitHub

**Dès que tout est ✅, on passe au déploiement ! 🚀**

---

**Créé le** : 6 janvier 2025  
**Projet** : Flowto - Automatisation Comptable PME  
**Domaine** : flowto.fr

