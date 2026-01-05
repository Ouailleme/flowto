# 🚀 Quick Start - Flowto

Bienvenue sur **Flowto** ! 🎉

---

## ⚡ Démarrage Rapide (3 étapes)

### 1. Créer les fichiers .env

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend  
cp frontend/.env.local.template frontend/.env.local
```

**Note** : Les valeurs par défaut fonctionnent en local !

### 2. Démarrer l'application

```bash
# Avec Make (recommandé)
make dev

# OU sans Make
docker-compose up -d
```

Attendez ~30 secondes que les services démarrent...

### 3. Ajouter des données de démo

```bash
make seed
```

---

## 🎯 Accès

| Service     | URL                              |
|-------------|----------------------------------|
| 🖥️ Frontend | http://localhost:3000            |
| ⚙️ Backend  | http://localhost:8000            |
| 📚 API Docs | http://localhost:8000/docs       |
| 🗄️ Database | localhost:5432 (flowto/flowto2026) |

---

## 🔑 Credentials de Démo

**Email** : `demo@flowto.fr`  
**Password** : `Demo123!`

Il y a aussi :
- `alice@startup.com` / `Alice123!`
- `bob@enterprise.com` / `Bob123!`

---

## 📋 Commandes Utiles

```bash
# Voir toutes les commandes disponibles
make help

# Arrêter l'app
make stop

# Voir les logs
make logs

# Lancer les tests
make test

# Formater le code
make format

# Health check
make health
```

---

## 🐛 En cas de problème

### Les containers ne démarrent pas ?

```bash
# Nettoyer et recommencer
docker-compose down -v
make dev
```

### Erreur de base de données ?

```bash
# Recréer la DB
docker-compose down -v
make dev
make seed
```

### Port déjà utilisé ?

Vérifiez que les ports 3000, 8000, 5432, 6379 sont libres.

---

## 📖 Documentation Complète

- **README** : Documentation principale
- **REBRANDING_FLOWTO.md** : Détails du renommage
- **PROJET_COMPLETE.md** : Fonctionnalités complètes
- **Makefile** : Liste des commandes (run `make help`)

---

## 🎨 Nouveau Design

Le projet s'appelle maintenant **Flowto** avec :
- 🌐 Domaine : **flowto.fr**
- 📧 Email : **@flowto.fr**
- 🎯 Nouvelle identité de marque

---

**Enjoy Flowto ! 🚀**

