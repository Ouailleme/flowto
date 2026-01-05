# 🌐 Guide d'Accès - FinanceAI

## 🚀 Le serveur est maintenant lancé !

Tous les services sont opérationnels et vous pouvez accéder au site.

---

## 🌐 URLs d'Accès

### Frontend (Next.js)
- **Page d'accueil** : http://localhost:3000
- **Page de connexion** : http://localhost:3000/auth/login
- **Dashboard** : http://localhost:3000/dashboard (après connexion)

### Backend (FastAPI)
- **API Documentation (Swagger)** : http://localhost:8000/docs
- **API Alternative (ReDoc)** : http://localhost:8000/redoc
- **Health Check** : http://localhost:8000/health

---

## 👤 Identifiants de Connexion

Utilisez ces identifiants pour vous connecter :

```
📧 Email:        demo@financeai.com
🔑 Mot de passe: Demo2026!
```

---

## ✅ Services Actifs

| Service | Port | Status |
|---------|------|--------|
| 🎨 Frontend (Next.js) | 3000 | ✅ Actif |
| ⚡ Backend (FastAPI) | 8000 | ✅ Actif |
| 🗄️ PostgreSQL | 5433 | ✅ Actif |
| 🔴 Redis | 6380 | ✅ Actif |

---

## 🎯 Comment Utiliser le Site

### 1. Accéder à la page d'accueil
Ouvrez votre navigateur et allez sur : http://localhost:3000

### 2. Se connecter
1. Cliquez sur "Commencer gratuitement" ou allez sur http://localhost:3000/auth/login
2. Entrez les identifiants :
   - Email : `demo@financeai.com`
   - Mot de passe : `Demo2026!`
3. Cliquez sur "Se connecter"

### 3. Explorer le Dashboard
Une fois connecté, vous serez redirigé vers le dashboard où vous pourrez :
- 📊 Voir les statistiques
- 💰 Gérer les factures
- 💳 Consulter les transactions
- ⚙️ Configurer les paramètres

---

## 📚 Fonctionnalités Disponibles

### ✅ Authentification
- ✅ Connexion
- ✅ Déconnexion
- ✅ Session persistante

### 📊 Dashboard
- ✅ Vue d'ensemble des statistiques
- ✅ Factures récentes
- ✅ Transactions récentes
- ✅ Navigation sidebar

### 💰 Factures
- ✅ Liste des factures
- ✅ Statistiques des factures
- ✅ Recherche
- ⚠️ Création (en cours)

### 💳 Transactions
- ✅ Liste des transactions
- ✅ Recherche
- ✅ Pagination
- ✅ Export
- ⚠️ Catégorisation (en cours)

### ⚙️ Paramètres
- ✅ Profil utilisateur
- ✅ Localisation
- ✅ Abonnement
- ✅ Notifications

---

## 🔧 Arrêter les Services

### Arrêter le Frontend
1. Allez dans le terminal PowerShell où le frontend tourne
2. Appuyez sur `Ctrl+C`

### Arrêter les Services Docker
```powershell
docker stop financeai_backend financeai_postgres financeai_redis
```

---

## 🆘 En Cas de Problème

### Le site ne charge pas
1. Vérifiez que le serveur frontend est bien lancé
2. Attendez 10-15 secondes après le démarrage
3. Rafraîchissez la page (F5)

### Impossible de se connecter
1. Vérifiez que vous utilisez les bons identifiants :
   - Email : `demo@financeai.com`
   - Mot de passe : `Demo2026!` (avec majuscule et point d'exclamation)
2. Vérifiez que le backend est actif : http://localhost:8000/health

### Erreur 404 ou 500
1. Vérifiez les logs du backend : `docker logs financeai_backend`
2. Vérifiez les logs du frontend dans le terminal PowerShell
3. Redémarrez les services si nécessaire

---

## 📈 Statistiques du Projet

- ✅ **Tests E2E** : 35/46 passés (76.1%)
- ✅ **Authentification** : Fonctionnelle
- ✅ **Backend API** : Opérationnel
- ✅ **Frontend** : Opérationnel
- ✅ **Base de données** : Configurée

---

## 🎉 Profitez de FinanceAI !

Votre application de comptabilité intelligente est maintenant prête à l'emploi.

Pour plus d'informations, consultez :
- **Rapport de tests** : `E2E_TESTS_SUCCESS_REPORT.md`
- **Documentation API** : http://localhost:8000/docs

---

*Dernière mise à jour : 5 janvier 2026*


