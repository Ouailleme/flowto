# ✅ Checklist de Test - Serveurs MCP

## 🎯 Objectif
Vérifier que tous les serveurs MCP sont correctement configurés et fonctionnels.

## 📋 Tests à Effectuer (Après Redémarrage de Cursor)

### 1. PostgreSQL MCP Server
**Status**: ⏳ À tester après redémarrage

**Commandes de test**:
```
1. "Liste toutes les tables de la base financeai"
2. "Montre-moi le schéma de la table users"
3. "Compte le nombre d'utilisateurs dans la base"
4. "Affiche les 5 dernières transactions"
```

**Résultat attendu**:
- ✅ Connexion réussie à PostgreSQL
- ✅ Liste des tables affichée
- ✅ Requêtes SQL exécutées correctement

**En cas d'erreur**:
- Vérifier que PostgreSQL est démarré
- Vérifier la connection string dans settings.json
- Tester manuellement: `psql -U postgres -d financeai`

---

### 2. Filesystem MCP Server
**Status**: ⏳ À tester après redémarrage

**Commandes de test**:
```
1. "Trouve tous les fichiers Python dans le backend"
2. "Montre-moi les modèles SQLAlchemy"
3. "Liste les composants React dans le frontend"
4. "Recherche les fichiers contenant 'FastAPI'"
```

**Résultat attendu**:
- ✅ Recherche sémantique fonctionne
- ✅ Fichiers trouvés avec contexte
- ✅ Suggestions pertinentes

**En cas d'erreur**:
- Vérifier le chemin dans settings.json: `C:\\Users\\yvesm\\Documents\\Projet`
- Vérifier les permissions du dossier

---

### 3. Memory MCP Server
**Status**: ⏳ À tester après redémarrage

**Commandes de test**:
```
1. "Rappelle-toi que nous utilisons bcrypt avec cost factor 12"
2. "Note que la limite de factures est 100,000 EUR"
3. "Mémorise que Bridge API a un rate limit de 100 req/min"
4. "Qu'est-ce que tu te rappelles sur bcrypt?"
```

**Résultat attendu**:
- ✅ Informations stockées
- ✅ Rappel correct des informations
- ✅ Persistance entre sessions

**En cas d'erreur**:
- Redémarrer Cursor
- Vérifier que le serveur memory est bien listé

---

### 4. Fetch MCP Server
**Status**: ⏳ À tester après redémarrage

**Commandes de test**:
```
1. "Teste l'endpoint http://localhost:8000/api/v1/health"
2. "Fais une requête GET sur https://api.github.com"
3. "Vérifie que l'API backend répond"
```

**Résultat attendu**:
- ✅ Requêtes HTTP exécutées
- ✅ Réponses affichées
- ✅ Headers et status codes visibles

**En cas d'erreur**:
- Vérifier la connexion internet
- Vérifier que le backend est démarré (si test local)

---

### 5. SQLite MCP Server
**Status**: ⏳ À tester après redémarrage

**Commandes de test**:
```
1. "Crée une table test_users dans SQLite"
2. "Insère un utilisateur de test"
3. "Sélectionne tous les utilisateurs de test"
4. "Supprime la table test_users"
```

**Résultat attendu**:
- ✅ Base SQLite créée à `C:\Users\yvesm\Documents\Projet\test.db`
- ✅ Opérations CRUD fonctionnent
- ✅ Requêtes SQL exécutées

**En cas d'erreur**:
- Vérifier les permissions d'écriture
- Vérifier le chemin dans settings.json

---

### 6. Puppeteer MCP Server
**Status**: ⏳ À tester après redémarrage

**Commandes de test**:
```
1. "Ouvre https://www.google.com avec Puppeteer"
2. "Prends un screenshot de la page"
3. "Navigue vers https://github.com"
```

**Résultat attendu**:
- ✅ Navigateur lancé
- ✅ Pages chargées
- ✅ Screenshots capturés

**En cas d'erreur**:
- Attendre l'installation de Chromium (première utilisation)
- Vérifier la connexion internet

---

### 7. GitHub MCP Server
**Status**: ⚠️ Nécessite GITHUB_TOKEN

**Configuration préalable**:
1. Créer un token sur https://github.com/settings/tokens
2. Ajouter dans settings.json: `"GITHUB_TOKEN": "ghp_votre_token"`
3. Redémarrer Cursor

**Commandes de test**:
```
1. "Liste mes repositories GitHub"
2. "Montre les issues ouvertes"
3. "Affiche les derniers commits"
```

**Résultat attendu**:
- ✅ Connexion à GitHub réussie
- ✅ Repositories listés
- ✅ Issues et commits affichés

**En cas d'erreur**:
- Vérifier le token et les scopes
- Vérifier que le token n'a pas expiré

---

### 8. Brave Search MCP Server
**Status**: ⚠️ Nécessite BRAVE_API_KEY

**Configuration préalable**:
1. Obtenir clé sur https://brave.com/search/api/
2. Ajouter dans settings.json: `"BRAVE_API_KEY": "BSA_votre_clé"`
3. Redémarrer Cursor

**Commandes de test**:
```
1. "Recherche 'FastAPI best practices' avec Brave"
2. "Trouve la documentation de SQLAlchemy 2.0"
3. "Cherche des exemples de Pydantic validators"
```

**Résultat attendu**:
- ✅ Recherches exécutées
- ✅ Résultats pertinents
- ✅ Snippets affichés

**En cas d'erreur**:
- Vérifier la clé API
- Vérifier le quota (gratuit = 2000 req/mois)

---

### 9. Slack MCP Server
**Status**: ⚠️ Nécessite SLACK_BOT_TOKEN (Optionnel)

**Configuration préalable**:
1. Créer une Slack App
2. Installer dans workspace
3. Copier le Bot Token
4. Ajouter dans settings.json
5. Redémarrer Cursor

**Commandes de test**:
```
1. "Liste les channels Slack"
2. "Envoie un message de test"
```

**Résultat attendu**:
- ✅ Connexion à Slack
- ✅ Channels listés
- ✅ Messages envoyés

---

### 10. Google Drive MCP Server
**Status**: ⚠️ Nécessite GOOGLE_CLIENT_ID (Optionnel)

**Configuration préalable**:
1. Créer projet Google Cloud
2. Activer API Drive
3. Créer credentials OAuth 2.0
4. Ajouter dans settings.json
5. Redémarrer Cursor

**Commandes de test**:
```
1. "Liste mes fichiers Google Drive"
2. "Recherche des documents"
```

**Résultat attendu**:
- ✅ Authentification OAuth réussie
- ✅ Fichiers listés
- ✅ Recherche fonctionne

---

## 📊 Résumé des Tests

### Serveurs Essentiels (Sans Configuration)
- [ ] PostgreSQL MCP Server
- [ ] Filesystem MCP Server
- [ ] Memory MCP Server
- [ ] Fetch MCP Server
- [ ] SQLite MCP Server
- [ ] Puppeteer MCP Server

### Serveurs Optionnels (Avec Tokens)
- [ ] GitHub MCP Server (Recommandé)
- [ ] Brave Search MCP Server (Utile)
- [ ] Slack MCP Server (Si équipe)
- [ ] Google Drive MCP Server (Si besoin)

## 🎯 Critères de Succès

### Minimum Viable (6/10 serveurs)
✅ Les 6 serveurs essentiels fonctionnent sans configuration

### Configuration Recommandée (7/10 serveurs)
✅ Les 6 essentiels + GitHub MCP

### Configuration Complète (10/10 serveurs)
✅ Tous les serveurs configurés et fonctionnels

## 🐛 Troubleshooting Global

### Les serveurs n'apparaissent pas
1. Vérifier que Cursor a été complètement redémarré
2. Vérifier le fichier settings.json
3. Vérifier les logs Cursor: `Help > Toggle Developer Tools > Console`

### Erreur "npx not found"
1. Installer Node.js: https://nodejs.org/
2. Vérifier: `node --version` et `npx --version`
3. Redémarrer Cursor

### Erreur de connexion
1. Vérifier la connexion internet
2. Vérifier les firewalls
3. Vérifier les proxies

## 📝 Notes de Test

Après avoir effectué les tests, notez ici les résultats:

```
Date du test: _____________
Version Cursor: _____________

Serveurs fonctionnels: ___/10

Problèmes rencontrés:
- 
- 
- 

Actions correctives:
- 
- 
- 
```

## 🚀 Prochaines Étapes

Une fois les tests validés:
1. ✅ Intégrer les MCP dans le workflow quotidien
2. ✅ Former l'équipe (si applicable)
3. ✅ Documenter les use cases spécifiques
4. ✅ Optimiser les configurations

---

**Action immédiate**: Redémarrer Cursor et commencer les tests!


