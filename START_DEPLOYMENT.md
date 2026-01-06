# 🚀 COMMENCE ICI - Déploiement Flowto

## ⚡ Quick Start (2 min)

### Étape 1 : Créer le Repo GitHub

1. **Va sur** : https://github.com/new
2. **Remplis** :
   - Repository name: `flowto`
   - Visibility: Private
   - ❌ **NE PAS** initialiser avec README
3. **Clique** : `Create repository`

---

### Étape 2 : Pusher le Code

**Copie ton username GitHub** (tu le vois en haut à droite sur GitHub)

**Puis exécute ces commandes** dans PowerShell (dans `C:\Users\yvesm\Documents\Projet`) :

```powershell
# Remplace [TON-USERNAME] par ton vrai username
git remote add origin https://github.com/[TON-USERNAME]/flowto.git
git branch -M main
git push -u origin main
```

**Exemple** :
```powershell
git remote add origin https://github.com/johndoe/flowto.git
git branch -M main
git push -u origin main
```

---

### Étape 3 : Vérifier

**Va sur** : `https://github.com/[TON-USERNAME]/flowto`

**Tu devrais voir** :
- ✅ Tous les fichiers du projet
- ✅ Le commit "🚀 Initial commit - Flowto v1.0 - Production ready"

---

## 🎯 Ensuite

**Une fois le code sur GitHub**, ouvre ces guides dans l'ordre :

1. `NEON_DATABASE_SETUP.md` (5 min)
2. `RENDER_BACKEND_SETUP.md` (15 min)
3. `VERCEL_FRONTEND_SETUP.md` (15 min)
4. `OVH_DOMAIN_SETUP.md` (30 min)

**Total** : 1h30 → Flowto en production !

---

## 🆘 Problèmes ?

### ❌ "remote origin already exists"

```powershell
git remote remove origin
git remote add origin https://github.com/[TON-USERNAME]/flowto.git
git push -u origin main
```

### ❌ "authentication failed"

1. Va sur : https://github.com/settings/tokens
2. `Generate new token` → `Tokens (classic)`
3. Scopes : ✅ repo (all), ✅ workflow
4. Copie le token
5. Utilise-le comme **mot de passe** lors du push

---

## ✅ Checklist Ultra-Rapide

- [ ] Repo GitHub créé
- [ ] Code pushé
- [ ] Visible sur GitHub

**Tout est ✅ ?** → Passe à `NEON_DATABASE_SETUP.md` ! 🚀

---

**Créé le** : 6 janvier 2025  
**Temps estimé** : 2 minutes

