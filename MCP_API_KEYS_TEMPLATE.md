# Configuration des Clés API pour MCP Servers

Ce document explique comment obtenir et configurer les clés API nécessaires pour les serveurs MCP.

## 1. GitHub Token (ESSENTIEL)

### Obtenir le token:
1. Aller sur: https://github.com/settings/tokens
2. Cliquer sur "Generate new token (classic)"
3. Sélectionner les scopes suivants:
   - `repo` (accès complet aux repositories)
   - `read:org` (lecture des organisations)
   - `read:user` (lecture du profil utilisateur)
4. Générer et copier le token

### Utilisation:
```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 2. Slack Bot Token (OPTIONNEL)

### Obtenir le token:
1. Aller sur: https://api.slack.com/apps
2. Créer une nouvelle app
3. Ajouter les scopes OAuth:
   - `chat:write`
   - `channels:read`
   - `files:write`
4. Installer l'app dans votre workspace
5. Copier le "Bot User OAuth Token"

### Utilisation:
```
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_TEAM_ID=T0XXXXXXXXX
```

## 3. Google Drive OAuth (OPTIONNEL)

### Obtenir les credentials:
1. Aller sur: https://console.cloud.google.com/
2. Créer un nouveau projet
3. Activer l'API Google Drive
4. Créer des credentials OAuth 2.0
5. Télécharger le fichier JSON

### Utilisation:
```
GOOGLE_CLIENT_ID=xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 4. Brave Search API (OPTIONNEL)

### Obtenir la clé:
1. Aller sur: https://brave.com/search/api/
2. S'inscrire pour un compte gratuit
3. Copier la clé API

### Utilisation:
```
BRAVE_API_KEY=BSAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 5. PostgreSQL Connection String (ESSENTIEL)

### Format:
```
postgresql://username:password@host:port/database
```

### Pour FinanceAI (local):
```
POSTGRES_CONNECTION_STRING=postgresql://postgres:postgres@localhost:5432/financeai
```

### Pour FinanceAI (production):
```
POSTGRES_CONNECTION_STRING=postgresql://user:password@your-db-host:5432/financeai
```

## Sécurité

⚠️ **IMPORTANT**: Ne jamais committer ces clés dans Git!

Ajoutez ces patterns au `.gitignore`:
```
.env.mcp
*_API_KEYS*
mcp-config.json
```

## Prochaines Étapes

Une fois les clés obtenues, vous devrez les configurer dans le fichier de configuration MCP de Cursor.


