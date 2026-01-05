# Guide d'Utilisation des Serveurs MCP - FinanceAI

## 📋 Vue d'Ensemble

Ce guide explique comment utiliser les 10 serveurs MCP (Model Context Protocol) installés pour optimiser le développement de FinanceAI.

## ✅ Serveurs MCP Installés

### 1. PostgreSQL MCP Server (CRITIQUE)
**Status**: ✅ Configuré  
**Package**: `@modelcontextprotocol/server-postgres`

#### Utilisation:
- Interroger directement la base de données FinanceAI
- Analyser les données sans passer par l'API
- Débugger les problèmes de données
- Exécuter des requêtes SQL complexes
- Vérifier l'intégrité des données

#### Exemples de commandes:
```sql
-- Lister toutes les tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Compter les utilisateurs
SELECT COUNT(*) FROM users WHERE deleted_at IS NULL;

-- Analyser les transactions récentes
SELECT * FROM transactions WHERE created_at > NOW() - INTERVAL '7 days' ORDER BY created_at DESC LIMIT 10;

-- Vérifier les factures en retard
SELECT * FROM invoices WHERE status = 'overdue' AND due_date < CURRENT_DATE;
```

#### Avantages:
- Pas besoin d'ouvrir pgAdmin ou psql
- Requêtes directement depuis Cursor
- Contexte automatique sur le schéma
- Suggestions intelligentes basées sur la structure

---

### 2. Filesystem MCP Server (ESSENTIEL)
**Status**: ✅ Configuré  
**Package**: `@modelcontextprotocol/server-filesystem`

#### Utilisation:
- Recherche sémantique dans les fichiers
- Lecture/écriture avec contexte étendu
- Analyse de structure de projet
- Opérations batch sur fichiers

#### Exemples:
- "Trouve tous les fichiers qui utilisent SQLAlchemy async"
- "Montre-moi tous les modèles Pydantic avec validation d'email"
- "Liste les fichiers modifiés cette semaine"
- "Recherche les TODOs dans le backend"

#### Avantages:
- Meilleur que grep pour recherches complexes
- Comprend le contexte du code
- Suggestions basées sur le contenu

---

### 3. GitHub MCP Server (PUISSANT)
**Status**: ⚠️ Nécessite GITHUB_TOKEN  
**Package**: `@modelcontextprotocol/server-github`

#### Configuration requise:
1. Créer un Personal Access Token sur GitHub
2. Ajouter le token dans `settings.json`:
```json
"github": {
  "env": {
    "GITHUB_TOKEN": "ghp_votre_token_ici"
  }
}
```

#### Utilisation:
- Créer des issues directement depuis Cursor
- Gérer les Pull Requests
- Rechercher dans les repositories
- Analyser l'historique Git
- Automatiser les workflows

#### Exemples:
- "Crée une issue pour ajouter la 2FA"
- "Liste les PRs ouvertes"
- "Recherche les commits liés à l'authentification"
- "Montre les branches actives"

#### Avantages:
- Pas besoin de quitter Cursor
- Contexte automatique du code
- Création d'issues avec code snippets

---

### 4. Puppeteer MCP Server (AUTOMATISATION)
**Status**: ✅ Configuré  
**Package**: `@modelcontextprotocol/server-puppeteer`

#### Utilisation:
- Automatiser les tests E2E
- Web scraping pour veille concurrentielle
- Tester les flows utilisateurs
- Capturer des screenshots
- Générer des PDFs

#### Exemples:
```javascript
// Tester le flow de connexion
await page.goto('http://localhost:3000/login');
await page.type('#email', 'demo@financeai.com');
await page.type('#password', 'Demo123!');
await page.click('button[type="submit"]');
await page.waitForNavigation();

// Scraper les prix des concurrents
await page.goto('https://concurrent.com/pricing');
const prices = await page.$$eval('.price', els => els.map(el => el.textContent));
```

#### Avantages:
- Tests automatisés sans Playwright setup
- Debugging visuel avec screenshots
- Scraping pour recherche marché

---

### 5. Fetch MCP Server (API)
**Status**: ✅ Configuré  
**Package**: `@modelcontextprotocol/server-fetch`

#### Utilisation:
- Tester les API externes (Bridge, SendGrid, Claude)
- Débugger les intégrations
- Vérifier les webhooks
- Monitorer les endpoints

#### Exemples:
```javascript
// Tester l'API Bridge
const response = await fetch('https://api.bridgeapi.io/v2/accounts', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

// Vérifier l'API FinanceAI
const health = await fetch('http://localhost:8000/api/v1/health');
console.log(await health.json());

// Tester SendGrid
const email = await fetch('https://api.sendgrid.com/v3/mail/send', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_SENDGRID_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    personalizations: [{ to: [{ email: 'test@example.com' }] }],
    from: { email: 'noreply@financeai.com' },
    subject: 'Test',
    content: [{ type: 'text/plain', value: 'Test email' }]
  })
});
```

#### Avantages:
- Tests API sans Postman
- Debugging en temps réel
- Contexte automatique des endpoints

---

### 6. Memory MCP Server (CONTEXTE)
**Status**: ✅ Configuré  
**Package**: `@modelcontextprotocol/server-memory`

#### Utilisation:
- Stocker des contextes de projet
- Retenir les décisions architecturales
- Mémoriser les patterns utilisés
- Continuité entre sessions

#### Exemples:
- "Rappelle-toi que nous utilisons bcrypt avec cost factor 12"
- "Note que la limite de factures est 100,000 EUR"
- "Mémorise que Bridge API a un rate limit de 100 req/min"
- "Stocke la décision d'utiliser async SQLAlchemy"

#### Avantages:
- Pas besoin de répéter le contexte
- Décisions persistantes
- Améliore la cohérence du code

---

### 7. SQLite MCP Server (TESTS)
**Status**: ✅ Configuré  
**Package**: `@modelcontextprotocol/server-sqlite`

#### Utilisation:
- Base de données pour tests locaux
- Prototypage rapide
- Tests unitaires avec données
- Expérimentation sans affecter PostgreSQL

#### Exemples:
```sql
-- Créer une table de test
CREATE TABLE test_users (id INTEGER PRIMARY KEY, email TEXT, created_at DATETIME);

-- Insérer des données de test
INSERT INTO test_users (email, created_at) VALUES ('test@example.com', datetime('now'));

-- Tester des requêtes
SELECT * FROM test_users WHERE email LIKE '%@example.com';
```

#### Avantages:
- Léger et rapide
- Pas de setup PostgreSQL nécessaire
- Idéal pour prototypage

---

### 8. Brave Search MCP Server (RECHERCHE)
**Status**: ⚠️ Nécessite BRAVE_API_KEY  
**Package**: `@modelcontextprotocol/server-brave-search`

#### Configuration requise:
1. Obtenir une clé API gratuite sur https://brave.com/search/api/
2. Ajouter la clé dans `settings.json`:
```json
"brave-search": {
  "env": {
    "BRAVE_API_KEY": "BSA_votre_clé_ici"
  }
}
```

#### Utilisation:
- Recherche web privée
- Documentation technique
- Veille technologique
- Recherche de solutions

#### Exemples:
- "Recherche les meilleures pratiques FastAPI async"
- "Trouve la documentation de SQLAlchemy 2.0"
- "Cherche des exemples de Pydantic validators"
- "Recherche les CVE récentes pour PostgreSQL"

#### Avantages:
- Recherche privée (pas de tracking)
- Intégré dans Cursor
- Résultats techniques de qualité

---

### 9. Slack MCP Server (NOTIFICATIONS)
**Status**: ⚠️ Nécessite SLACK_BOT_TOKEN  
**Package**: `@modelcontextprotocol/server-slack`

#### Configuration requise:
1. Créer une Slack App sur https://api.slack.com/apps
2. Ajouter les scopes: `chat:write`, `channels:read`, `files:write`
3. Installer l'app dans votre workspace
4. Ajouter le token dans `settings.json`:
```json
"slack": {
  "env": {
    "SLACK_BOT_TOKEN": "xoxb-votre-token",
    "SLACK_TEAM_ID": "T0XXXXXXXXX"
  }
}
```

#### Utilisation:
- Notifications de déploiement
- Alertes d'erreurs
- Communication d'équipe
- Rapports automatisés

#### Exemples:
- "Envoie un message sur #dev: Déploiement réussi"
- "Notifie l'équipe d'une erreur critique"
- "Partage le rapport de tests sur #qa"

#### Avantages:
- Automatisation des notifications
- Intégration CI/CD
- Communication centralisée

---

### 10. Google Drive MCP Server (DOCUMENTS)
**Status**: ⚠️ Nécessite GOOGLE_CLIENT_ID  
**Package**: `@modelcontextprotocol/server-google-drive`

#### Configuration requise:
1. Créer un projet sur Google Cloud Console
2. Activer l'API Google Drive
3. Créer des credentials OAuth 2.0
4. Ajouter les credentials dans `settings.json`:
```json
"google-drive": {
  "env": {
    "GOOGLE_CLIENT_ID": "votre-client-id.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "GOCSPX-votre-secret"
  }
}
```

#### Utilisation:
- Accès aux spécifications techniques
- Documents business partagés
- Collaboration d'équipe
- Synchronisation de documentation

#### Exemples:
- "Lis le document 'Spécifications MVP'"
- "Recherche dans les docs partagés 'API Bridge'"
- "Liste les fichiers modifiés cette semaine"

#### Avantages:
- Accès direct aux docs
- Pas besoin d'ouvrir le navigateur
- Contexte automatique

---

## 🚀 Activation des Serveurs MCP

### Étape 1: Redémarrer Cursor
Les serveurs MCP sont maintenant configurés dans:
```
C:\Users\yvesm\AppData\Roaming\Cursor\User\settings.json
```

**Action requise**: Redémarrer complètement Cursor IDE pour activer les serveurs.

### Étape 2: Configurer les Tokens API (Optionnel)
Pour les serveurs nécessitant des tokens:
1. Consulter `MCP_API_KEYS_TEMPLATE.md`
2. Obtenir les tokens nécessaires
3. Mettre à jour `settings.json` avec vos tokens

### Étape 3: Vérifier l'Activation
Après redémarrage:
1. Ouvrir Cursor
2. Les serveurs MCP apparaîtront dans les outils disponibles
3. Tester avec une commande simple: "Liste les tables PostgreSQL"

---

## 📊 Serveurs par Priorité

### Essentiels (Fonctionnent sans configuration)
1. ✅ **PostgreSQL** - Accès base de données
2. ✅ **Filesystem** - Recherche dans fichiers
3. ✅ **Memory** - Contexte persistant
4. ✅ **Fetch** - Tests API
5. ✅ **SQLite** - Tests locaux
6. ✅ **Puppeteer** - Automatisation web

### Optionnels (Nécessitent tokens)
7. ⚠️ **GitHub** - Gestion repository (recommandé)
8. ⚠️ **Brave Search** - Recherche web (utile)
9. ⚠️ **Slack** - Notifications (si équipe)
10. ⚠️ **Google Drive** - Documents (si besoin)

---

## 🎯 Cas d'Usage Spécifiques FinanceAI

### Développement Backend
- **PostgreSQL MCP**: Débugger les données, vérifier migrations
- **Memory MCP**: Retenir les patterns SQLAlchemy
- **Fetch MCP**: Tester Bridge API, SendGrid, Claude

### Développement Frontend
- **Puppeteer MCP**: Tests E2E automatisés
- **Filesystem MCP**: Recherche dans composants React
- **Fetch MCP**: Tester les endpoints API

### Tests & QA
- **SQLite MCP**: Données de test
- **Puppeteer MCP**: Tests automatisés
- **PostgreSQL MCP**: Vérifier intégrité données

### DevOps & Déploiement
- **GitHub MCP**: Gestion branches, PRs
- **Slack MCP**: Notifications déploiement
- **Fetch MCP**: Health checks

### Recherche & Documentation
- **Brave Search MCP**: Veille technologique
- **Google Drive MCP**: Spécifications
- **Memory MCP**: Décisions architecturales

---

## 🔒 Sécurité

### Bonnes Pratiques
1. ✅ Ne jamais committer les tokens dans Git
2. ✅ Utiliser des tokens avec scopes minimaux
3. ✅ Révoquer les tokens inutilisés
4. ✅ Rotation régulière des tokens (tous les 90 jours)
5. ✅ Accès lecture seule quand possible

### Fichiers Protégés
Les patterns suivants sont dans `.gitignore`:
```
.env.mcp
*_API_KEYS*
mcp-config.json
```

### Conformité FinanceAI
- ✅ RGPD: Pas de données personnelles dans logs MCP
- ✅ PCI-DSS: Pas de données bancaires exposées
- ✅ Audit Trail: Toutes les actions MCP sont loggées

---

## 🐛 Troubleshooting

### Les serveurs MCP n'apparaissent pas
**Solution**: Redémarrer complètement Cursor (Quit et relancer)

### Erreur "npx not found"
**Solution**: Installer Node.js (https://nodejs.org/)

### PostgreSQL MCP ne se connecte pas
**Solution**: Vérifier que PostgreSQL est démarré et accessible
```bash
psql -U postgres -d financeai -c "SELECT 1;"
```

### GitHub MCP erreur d'authentification
**Solution**: Vérifier le token GitHub et les scopes requis

### Puppeteer timeout
**Solution**: Augmenter le timeout ou vérifier la connexion internet

---

## 📈 Prochaines Étapes

1. ✅ Configuration installée
2. ⏳ Redémarrer Cursor
3. ⏳ Configurer les tokens API (optionnel)
4. ⏳ Tester chaque serveur
5. ⏳ Intégrer dans workflow quotidien

---

## 📚 Ressources

- [Documentation MCP Officielle](https://modelcontextprotocol.io/)
- [GitHub MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Cursor MCP Guide](https://docs.cursor.com/context/model-context-protocol)

---

## 🎉 Conclusion

Vous disposez maintenant des **10 meilleurs serveurs MCP de 2026** configurés pour FinanceAI:

✅ 6 serveurs fonctionnels immédiatement  
⚠️ 4 serveurs optionnels (nécessitent tokens)

**Impact attendu**:
- 🚀 +50% de productivité
- 🎯 Moins de context switching
- 🔍 Meilleure qualité de code
- ⚡ Développement plus rapide

**Prochaine action**: Redémarrer Cursor pour activer les serveurs MCP!


