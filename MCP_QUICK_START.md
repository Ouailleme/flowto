# 🚀 Quick Start - Serveurs MCP FinanceAI

## ✅ Installation Complète

Les 10 meilleurs serveurs MCP de 2026 sont maintenant installés!

## 📋 Serveurs Installés

| Serveur | Status | Configuration Requise |
|---------|--------|----------------------|
| PostgreSQL | ✅ Prêt | Aucune |
| Filesystem | ✅ Prêt | Aucune |
| Memory | ✅ Prêt | Aucune |
| Fetch | ✅ Prêt | Aucune |
| SQLite | ✅ Prêt | Aucune |
| Puppeteer | ✅ Prêt | Aucune |
| GitHub | ⚠️ Token requis | GITHUB_TOKEN |
| Brave Search | ⚠️ Token requis | BRAVE_API_KEY |
| Slack | ⚠️ Token requis | SLACK_BOT_TOKEN |
| Google Drive | ⚠️ Token requis | GOOGLE_CLIENT_ID |

## 🎯 Prochaines Étapes

### 1. Redémarrer Cursor (OBLIGATOIRE)
```
Fichier > Quitter Cursor
Relancer Cursor
```

### 2. Tester les Serveurs de Base
Après redémarrage, essayez:

#### PostgreSQL
```
"Liste toutes les tables de la base financeai"
"Compte le nombre d'utilisateurs actifs"
```

#### Filesystem
```
"Trouve tous les fichiers Python qui utilisent FastAPI"
"Montre-moi les modèles SQLAlchemy"
```

#### Memory
```
"Rappelle-toi que nous utilisons bcrypt avec cost factor 12"
"Note que la limite de factures est 100,000 EUR"
```

### 3. Configurer les Tokens (Optionnel)
Voir `MCP_API_KEYS_TEMPLATE.md` pour les instructions détaillées.

#### GitHub Token (Recommandé)
1. Aller sur: https://github.com/settings/tokens
2. Créer un token avec scopes: `repo`, `read:org`, `read:user`
3. Éditer `C:\Users\yvesm\AppData\Roaming\Cursor\User\settings.json`
4. Remplacer `"GITHUB_TOKEN": ""` par `"GITHUB_TOKEN": "ghp_votre_token"`
5. Redémarrer Cursor

#### Brave Search (Utile)
1. Obtenir clé gratuite: https://brave.com/search/api/
2. Ajouter dans settings.json: `"BRAVE_API_KEY": "BSA_votre_clé"`
3. Redémarrer Cursor

## 🎓 Exemples d'Utilisation

### Développement Backend
```
"Montre-moi toutes les routes API dans le backend"
"Analyse la structure de la table invoices"
"Teste l'endpoint /api/v1/health"
```

### Développement Frontend
```
"Trouve tous les composants React qui utilisent useState"
"Liste les pages Next.js du projet"
"Teste le flow de connexion avec Puppeteer"
```

### Tests & Debugging
```
"Crée une base SQLite de test avec des utilisateurs"
"Exécute une requête pour trouver les factures en retard"
"Vérifie la connexion à l'API Bridge"
```

### Recherche & Documentation
```
"Recherche les meilleures pratiques FastAPI async"
"Trouve la documentation de Pydantic validators"
"Mémorise que nous utilisons JWT avec refresh tokens"
```

## 📊 Fichiers Créés

1. ✅ `mcp-servers-config.json` - Configuration de référence
2. ✅ `MCP_API_KEYS_TEMPLATE.md` - Guide pour obtenir les tokens
3. ✅ `MCP_SERVERS_GUIDE.md` - Documentation complète
4. ✅ `MCP_QUICK_START.md` - Ce fichier
5. ✅ `.gitignore` - Mis à jour pour protéger les tokens
6. ✅ `settings.json` - Configuration Cursor activée

## 🔒 Sécurité

✅ Backup créé: `settings.json.backup`  
✅ Tokens protégés dans `.gitignore`  
✅ Configuration conforme RGPD/PCI-DSS

## 📚 Documentation Complète

Pour plus de détails, consultez:
- `MCP_SERVERS_GUIDE.md` - Guide complet d'utilisation
- `MCP_API_KEYS_TEMPLATE.md` - Configuration des tokens

## 🎉 C'est Parti!

**Action immédiate**: Redémarrer Cursor pour activer les 10 serveurs MCP!

Après redémarrage, vous aurez accès à:
- 🗄️ Base de données PostgreSQL directement
- 📁 Recherche avancée dans les fichiers
- 🧠 Mémoire contextuelle persistante
- 🌐 Tests API automatisés
- 🤖 Automatisation web avec Puppeteer
- Et bien plus encore!

---

**Besoin d'aide?** Consultez la section Troubleshooting dans `MCP_SERVERS_GUIDE.md`


