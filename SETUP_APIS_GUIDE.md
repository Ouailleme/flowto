# 🔑 Guide Configuration APIs - Flowto

Guide pratique pour configurer toutes les APIs externes.

---

## 📋 APIs Nécessaires

| Service | Fonction | Prix | Priorité |
|---------|----------|------|----------|
| Bridge API | Agrégation bancaire | Gratuit (dev) | 🔴 Haute |
| Anthropic | IA (catégorisation) | ~5€/mois | 🟡 Moyenne |
| SendGrid | Envoi emails | Gratuit (100/jour) | 🟢 Basse |
| Sentry | Error tracking | Gratuit (5k events) | 🔴 Haute |

---

## 1️⃣ Bridge API (Agrégation Bancaire)

### Inscription (5 min)

1. **Créer compte** : https://dashboard.bridgeapi.io/signup
   - Email professionnel
   - Nom de l'entreprise : Flowto
   - Cas d'usage : SaaS comptabilité PME

2. **Vérification email**

3. **Dashboard** → Obtenir API Key
   - Mode : Sandbox (pour développement)
   - Production : demander activation

### Configuration

```bash
# Dans Render (Backend)
BRIDGE_API_KEY=your_bridge_api_key_here
BRIDGE_API_URL=https://api.bridgeapi.io/v2
```

### Test

```bash
# Depuis votre terminal local
curl -X GET "https://api.bridgeapi.io/v2/banks" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Client-Id: YOUR_CLIENT_ID" \
  -H "Client-Secret: YOUR_CLIENT_SECRET"
```

### Features Disponibles

- ✅ Connexion à 400+ banques
- ✅ Récupération transactions
- ✅ Soldes comptes
- ✅ Catégorisation basique
- ✅ Webhooks (notifications)

### Webhook Configuration

```bash
# URL à configurer dans Bridge Dashboard
https://api.flowto.fr/webhooks/bridge

# Events à écouter :
- transaction.created
- account.updated
- transaction.updated
```

---

## 2️⃣ Anthropic Claude (IA)

### Inscription (3 min)

1. **Créer compte** : https://console.anthropic.com
   - Email
   - Vérification

2. **API Keys** → Create Key
   - Name : Flowto Production
   - Copier la clé (une seule fois visible !)

### Configuration

```bash
# Dans Render (Backend)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### Test

```bash
# Depuis Python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-api03-...")
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Catégorise : Achat Carrefour 45.23€"}
    ]
)
print(message.content)
```

### Usage Estimé

```
Catégorisation transaction : ~500 tokens (~$0.0015)
100 transactions/jour : ~$0.15/jour = $4.50/mois
```

### Limites Gratuites

- ❌ Pas de tier gratuit Anthropic
- ✅ Pay-as-you-go dès $1
- ✅ $5 offerts à l'inscription
- 💡 Alternative gratuite : OpenAI (50k tokens gratuits/mois)

---

## 3️⃣ SendGrid (Emails)

### Inscription (5 min)

1. **Créer compte** : https://signup.sendgrid.com
   - Email
   - Nom de l'entreprise : Flowto
   - Type : SaaS
   - Pas de CB requise (Free : 100 emails/jour)

2. **Vérifier email**

3. **Settings** → API Keys → Create API Key
   - Name : Flowto Production
   - Permissions : Full Access (pour commencer)
   - Copier la clé

### Vérification Domaine (15 min)

**Important pour éviter SPAM !**

1. **Settings** → Sender Authentication
2. **Authenticate Your Domain** → flowto.fr
3. **DNS Records à ajouter** (chez OVH/Cloudflare) :

```dns
# SPF Record
Type: TXT
Name: @
Value: v=spf1 include:sendgrid.net ~all

# DKIM Records (SendGrid fournit les valeurs)
Type: CNAME
Name: s1._domainkey
Value: s1.domainkey.u12345678.wl123.sendgrid.net

Type: CNAME
Name: s2._domainkey
Value: s2.domainkey.u12345678.wl123.sendgrid.net

# DMARC Record
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc@flowto.fr
```

4. **Vérifier** (peut prendre 24-48h)

### Configuration

```bash
# Dans Render (Backend)
SENDGRID_API_KEY=SG.your-api-key-here
SENDGRID_FROM_EMAIL=noreply@flowto.fr
```

### Test

```bash
# Depuis Python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='noreply@flowto.fr',
    to_emails='test@example.com',
    subject='Test Flowto',
    html_content='<strong>Ça marche !</strong>')

sg = SendGridAPIClient('SG.your-api-key')
response = sg.send(message)
print(response.status_code)
```

### Templates Email à Créer

1. **Welcome Email** (Inscription)
2. **Invoice Reminder** (Relance facture)
3. **Payment Confirmation** (Paiement reçu)
4. **Password Reset** (Mot de passe oublié)
5. **Weekly Digest** (Résumé hebdomadaire)

### Limites

```
Free       : 100 emails/jour (suffisant pour démarrer)
Essentials : 15€/mois → 40,000 emails/mois
Pro        : 90€/mois → 100,000 emails/mois
```

---

## 4️⃣ Sentry (Error Tracking)

### Inscription (3 min)

1. **Créer compte** : https://sentry.io/signup
   - Email
   - Pas de CB requise

2. **Create Organization** : Flowto

### Projet Backend (Python/FastAPI)

1. **Create Project**
   - Platform : **Python**
   - Project name : **flowto-backend**

2. **Copier DSN** :
   ```
   https://abcd1234@o123456.ingest.sentry.io/7654321
   ```

3. **Installer SDK** (déjà fait dans requirements.txt) :
   ```bash
   pip install sentry-sdk[fastapi]
   ```

### Projet Frontend (Next.js)

1. **Create Project**
   - Platform : **Next.js**
   - Project name : **flowto-frontend**

2. **Copier DSN** :
   ```
   https://efgh5678@o123456.ingest.sentry.io/7654322
   ```

3. **Installer SDK** :
   ```bash
   cd frontend
   npm install @sentry/nextjs
   npx @sentry/wizard -i nextjs
   ```

### Configuration

**Backend (Render)** :
```bash
SENTRY_DSN=https://abcd1234@o123456.ingest.sentry.io/7654321
SENTRY_ENVIRONMENT=production
```

**Frontend (Vercel)** :
```bash
NEXT_PUBLIC_SENTRY_DSN=https://efgh5678@o123456.ingest.sentry.io/7654322
NEXT_PUBLIC_ENVIRONMENT=production
```

### Test

**Backend** :
```python
# Test error
import sentry_sdk
sentry_sdk.capture_exception(Exception("Test Sentry Backend"))
```

**Frontend** :
```javascript
// pages/test-sentry.tsx
throw new Error("Test Sentry Frontend");
```

### Configuration Alertes

1. **Alerts** → New Alert Rule
2. **Conditions** :
   - When error count > 10 in 1 hour
   - When new error appears
   - When error rate > 5%
3. **Actions** :
   - Email notification
   - Slack notification (optionnel)

### Limites

```
Free      : 5,000 events/mois (largement suffisant)
Team      : 26€/mois → 50,000 events
Business  : 80€/mois → 500,000 events
```

---

## 5️⃣ Upstash Redis (Cache) - Optionnel

### Inscription (2 min)

1. **Créer compte** : https://upstash.com
2. **Create Database**
   - Name : flowto-cache
   - Region : eu-west-1 (Irlande)
   - Type : Redis

3. **Copier connection string** :
   ```
   rediss://default:password@hostname:6379
   ```

### Configuration

```bash
# Dans Render (Backend)
REDIS_URL=rediss://default:password@hostname:6379
```

### Limites

```
Free : 10,000 commandes/jour
Pay-as-you-go : $0.20 par 100k commandes
```

---

## 🔐 Gestion des Secrets

### ⚠️ IMPORTANT : Sécurité

**Ne JAMAIS commit** :
- ❌ API keys dans le code
- ❌ Fichiers .env dans Git
- ❌ Secrets dans les logs

**Bonnes pratiques** :
- ✅ Variables d'environnement (Render, Vercel)
- ✅ Fichiers .env en .gitignore
- ✅ Rotation des clés tous les 3-6 mois
- ✅ Clés différentes dev/staging/prod

### Rotation des Clés (tous les 6 mois)

```bash
# 1. Créer nouvelle clé
# 2. Ajouter nouvelle clé dans Render/Vercel
# 3. Tester en production
# 4. Supprimer ancienne clé
# 5. Documenter dans 1Password/Vault
```

---

## 📊 Dashboard Centralisé (Optionnel)

### Créer un Google Sheet pour suivre :

| Service | Status | API Key | Expire | Cost/mois | Notes |
|---------|--------|---------|--------|-----------|-------|
| Bridge | ✅ | bri_xxx... | - | 0€ | Sandbox |
| Anthropic | ✅ | sk-ant... | - | ~5€ | 100 tx/j |
| SendGrid | ✅ | SG.xxx... | - | 0€ | 100 emails/j |
| Sentry Backend | ✅ | https... | - | 0€ | 5k events |
| Sentry Frontend | ✅ | https... | - | 0€ | 5k events |
| Upstash | ⏸️ | redis... | - | 0€ | Optionnel |

---

## ✅ Checklist Finale

### APIs Configurées
- [ ] Bridge API - Compte créé
- [ ] Bridge API - API key obtenue
- [ ] Bridge API - Webhook configuré
- [ ] Anthropic - Compte créé
- [ ] Anthropic - API key obtenue
- [ ] SendGrid - Compte créé
- [ ] SendGrid - API key obtenue
- [ ] SendGrid - Domaine vérifié (SPF/DKIM)
- [ ] Sentry Backend - Projet créé
- [ ] Sentry Frontend - Projet créé
- [ ] Sentry - Alertes configurées

### Variables d'Environnement
- [ ] Render - Toutes les variables ajoutées
- [ ] Vercel - Toutes les variables ajoutées
- [ ] Backend redéployé avec nouvelles vars
- [ ] Frontend redéployé avec nouvelles vars

### Tests
- [ ] Bridge - Connexion test OK
- [ ] Anthropic - Catégorisation test OK
- [ ] SendGrid - Email test envoyé et reçu
- [ ] Sentry Backend - Error test capturée
- [ ] Sentry Frontend - Error test capturée

---

## 🆘 Troubleshooting

### Bridge API : 401 Unauthorized
```bash
# Vérifier que la clé est bien configurée
echo $BRIDGE_API_KEY
# Vérifier dans Bridge Dashboard : clé active
```

### SendGrid : Emails en SPAM
```bash
# Vérifier SPF/DKIM records
dig TXT flowto.fr
dig CNAME s1._domainkey.flowto.fr
# Attendre 24-48h après config DNS
```

### Sentry : Pas d'events
```bash
# Vérifier DSN configuré
echo $SENTRY_DSN
# Vérifier import Sentry dans app/main.py
# Tester manuellement : sentry_sdk.capture_exception()
```

### Anthropic : Rate Limit
```bash
# Limites Tier 1 : 50 req/min
# Solution : implémenter queue + retry
# Alternative : cacher les catégories fréquentes
```

---

**Toutes les APIs sont maintenant configurées ! 🎉**

**Temps total : ~30-45 minutes**

