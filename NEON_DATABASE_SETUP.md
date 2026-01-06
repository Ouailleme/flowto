# 🗄️ Setup Database Neon pour Flowto

## Pourquoi Neon ?
- ✅ **Gratuit** : 500 MB inclus (largement suffisant pour commencer)
- ✅ **Serverless** : PostgreSQL moderne, auto-scaling
- ✅ **Europe** : Serveurs en Europe (RGPD-friendly)
- ✅ **Simple** : Setup en 5 minutes

---

## 📝 Étapes

### 1️⃣ Créer un Compte Neon (2 min)

1. **Va sur** : https://neon.tech
2. **Clique sur** : `Sign up`
3. **Choisis** : `Continue with GitHub` (le plus rapide)
4. **Autorise** Neon à accéder à ton compte GitHub

✅ **Tu es maintenant connecté à Neon !**

---

### 2️⃣ Créer un Projet (2 min)

1. **Neon te redirige vers** : Create a new project
2. **Remplis** :
   ```
   Project name: flowto
   PostgreSQL version: 16 (dernière version)
   Region: Frankfurt (eu-central-1) ou Amsterdam (eu-west-1)
   ```
3. **Clique sur** : `Create project`

⏳ **Attends 10-15 secondes** (création du projet)

---

### 3️⃣ Obtenir la Connection String (1 min)

Une fois le projet créé, tu arrives sur le **Dashboard**.

1. **Va dans** : `Dashboard` → `Connection Details`
2. **Tu verras plusieurs formats** :
   - Connection string
   - Pooled connection
   - Direct connection

3. **Copie** : `Connection string` (le premier)
   ```
   Format : postgresql://username:password@host/database
   ```

4. **Exemple** :
   ```
   postgresql://flowto_user:AbCdEfGh123456@ep-cool-name-123456.eu-central-1.aws.neon.tech/flowto?sslmode=require
   ```

---

### 4️⃣ Adapter la Connection String pour FastAPI

⚠️ **IMPORTANT** : FastAPI avec SQLAlchemy async nécessite `postgresql+asyncpg://` au lieu de `postgresql://`

**Remplace** :
```
postgresql://...
```

**Par** :
```
postgresql+asyncpg://...
```

**Exemple final** :
```
postgresql+asyncpg://flowto_user:AbCdEfGh123456@ep-cool-name-123456.eu-central-1.aws.neon.tech/flowto?sslmode=require
```

✅ **Copie cette connection string modifiée**, tu en auras besoin pour Render !

---

### 5️⃣ Tester la Connexion (Optionnel)

**Dans Neon Dashboard** → `SQL Editor`, teste :

```sql
-- Créer une table test
CREATE TABLE test_connection (
    id SERIAL PRIMARY KEY,
    message TEXT
);

-- Insérer une donnée
INSERT INTO test_connection (message) VALUES ('Flowto is ready!');

-- Vérifier
SELECT * FROM test_connection;
```

**Tu devrais voir** :
```
| id | message            |
|----|-------------------|
| 1  | Flowto is ready!  |
```

✅ **Si ça marche → Ta database est prête !**

---

## 📋 Informations Importantes

### 🔑 Credentials

**Database** : `flowto`  
**User** : `flowto_user` (ou autre nom généré)  
**Host** : `ep-xxxxx.eu-central-1.aws.neon.tech`  
**Port** : `5432` (défaut PostgreSQL)

### 📊 Limites Gratuites

- **Storage** : 500 MB (amplement suffisant pour démarrer)
- **Compute** : 100 heures/mois
- **Branches** : 1 (main)

### 🔒 Sécurité

- ✅ SSL obligatoire (`?sslmode=require`)
- ✅ Mots de passe générés automatiquement
- ✅ Accès restreint par IP (configurable)

---

## ✅ Checklist

- [ ] Compte Neon créé
- [ ] Projet `flowto` créé
- [ ] Region : Europe (Frankfurt ou Amsterdam)
- [ ] Connection string copiée
- [ ] Connection string modifiée (postgresql+asyncpg://)
- [ ] Test de connexion OK (optionnel)

---

## 🎯 Prochaine Étape

**Connection string prête ?** → On configure le backend sur Render ! 🚀

**Format à garder** :
```
postgresql+asyncpg://[user]:[password]@[host]/[database]?sslmode=require
```

---

## 🆘 Problèmes Courants

### ❌ Erreur : "SSL connection required"

**Solution** : Ajoute `?sslmode=require` à la fin de l'URL

### ❌ Erreur : "password authentication failed"

**Solution** : Vérifie que tu as bien copié tout le mot de passe (souvent très long)

### ❌ Database trop lente

**Solution** : 
- Plan gratuit : Cold start possible (1-2 secondes)
- Upgrade vers plan Pro si nécessaire (19$/mois)

---

**Créé le** : 6 janvier 2025  
**Projet** : Flowto - Automatisation Comptable PME  
**Stack** : PostgreSQL 16 + Neon Serverless

