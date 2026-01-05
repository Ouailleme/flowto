# FinanceAI - Setup Guide

## 🚀 Quick Start

Ce guide vous permet de démarrer le développement de FinanceAI en **Phase 1 (MVP No-Code)**.

---

## Phase 1: MVP No-Code (Semaines 1-8)

### Prérequis

**Comptes à créer** (gratuits ou essai):
- [ ] [Bubble.io](https://bubble.io) - Frontend no-code
- [ ] [Make.com](https://make.com) - Workflow automation
- [ ] [Supabase](https://supabase.com) - Database PostgreSQL
- [ ] [Bridge API](https://bridgeapi.io) - Agrégateur bancaire
- [ ] [Anthropic](https://console.anthropic.com) - Claude API
- [ ] [SendGrid](https://sendgrid.com) - Emails transactionnels
- [ ] [Stripe](https://stripe.com) - Paiements

**Outils développement**:
- [ ] Git
- [ ] VS Code ou Cursor
- [ ] Compte GitHub

### Étape 1: Validation (Semaine 1) ✅

**Si pas encore fait:**

1. **Landing Page**
```bash
# Créer landing page sur Carrd.co ou Framer
# Template: SaaS B2B
# Headline: "Automatisez votre comptabilité PME en 30 minutes"
# Pricing visible: 399€/mois
# CTA: "Rejoindre la liste d'attente"
```

2. **Ads Budget: 400€**
- Google Ads: 200€ (mots-clés "automatisation comptable PME")
- LinkedIn Ads: 200€ (cible CFO/DAF/gérants)

3. **Interviews: 15-20 prospects**
- Script dans `validation_strategy.md`
- Objectif: Valider WTP > 400€/mois

4. **Pre-sales: Founder Pass**
- 199€/mois (lifetime 50% off)
- Objectif: 5-10 pré-ventes

**Critères GO**: 30+ emails waitlist, 60%+ "would use", 5+ pre-sales

---

### Étape 2: Setup Infrastructure (Semaine 2)

#### 2.1 Domaines & Email
```bash
# Acheter domaine
# Recommandé: financeai.fr ou similaire
# Provider: OVH, Gandi, Namecheap

# Setup email professionnel
# Google Workspace: 6€/mois/user
# Email: contact@financeai.fr, support@financeai.fr
```

#### 2.2 Database (Supabase)

1. Créer projet Supabase: https://app.supabase.com
2. Copier Database URL
3. Exécuter schema SQL:

```sql
-- Voir fichier: database_schema.sql (à créer)
-- Ou copier depuis ROADMAP_FINANCE_PME.md
```

#### 2.3 Bridge API (Banking)

1. Créer compte: https://dashboard.bridgeapi.io
2. Mode Sandbox (gratuit pour dev)
3. Obtenir:
   - Client ID
   - Client Secret
   - API Key

4. Tester connexion:
```bash
curl -X POST https://api.bridgeapi.io/v2/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
  }'
```

#### 2.4 Claude API (Anthropic)

1. Créer compte: https://console.anthropic.com
2. Obtenir API Key
3. Crédits gratuits: 5$ (suffisant pour tests)

4. Tester:
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Categorize this transaction: VIREMENT LOYER BUREAU - 1500 EUR"}
    ]
  }'
```

#### 2.5 SendGrid (Emails)

1. Créer compte: https://sendgrid.com
2. Plan gratuit: 100 emails/jour
3. Créer API Key
4. Vérifier domaine (pour éviter spam)

#### 2.6 Variables d'Environnement

Créer fichier `.env` (JAMAIS commit!):
```bash
# Database
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_supabase_key
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres

# Bridge API
BRIDGE_CLIENT_ID=your_client_id
BRIDGE_CLIENT_SECRET=your_client_secret
BRIDGE_API_KEY=your_api_key
BRIDGE_ENV=sandbox  # or production

# Claude API
ANTHROPIC_API_KEY=sk-ant-xxx

# SendGrid
SENDGRID_API_KEY=SG.xxx
SENDGRID_FROM_EMAIL=noreply@financeai.fr

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# App
APP_NAME=FinanceAI
APP_URL=https://financeai.fr
ENVIRONMENT=development
```

---

### Étape 3: Bubble.io Setup (Semaines 3-4)

#### 3.1 Créer App Bubble

1. Aller sur https://bubble.io/build
2. Créer nouvelle app: "FinanceAI"
3. Template: Blank (on part from scratch)

#### 3.2 Setup Database dans Bubble

**Data Types à créer**:
1. **User** (built-in, customiser)
   - company_name (text)
   - company_size (text)
   - subscription_plan (text)
   - subscription_status (text)

2. **BankAccount**
   - user (User)
   - bridge_account_id (text)
   - bank_name (text)
   - account_type (text)
   - balance (number)
   - last_sync_at (date)

3. **Transaction**
   - bank_account (BankAccount)
   - bridge_transaction_id (text)
   - date (date)
   - description (text)
   - amount (number)
   - category (text)
   - is_reconciled (yes/no)

4. **Invoice**
   - user (User)
   - invoice_number (text)
   - client_name (text)
   - client_email (text)
   - amount (number)
   - due_date (date)
   - status (text)
   - is_reconciled (yes/no)

5. **Reconciliation**
   - user (User)
   - transaction (Transaction)
   - invoice (Invoice)
   - match_score (number)
   - validated_at (date)

#### 3.3 Pages à créer

1. **index** (homepage logged out)
2. **login** (auth)
3. **signup** (auth)
4. **dashboard** (main app)
5. **transactions** (list + detail)
6. **invoices** (list + detail)
7. **reconciliations** (validation)
8. **settings** (user settings)

---

### Étape 4: Make.com Setup (Semaines 3-4)

#### 4.1 Créer Compte Make

1. https://make.com/register
2. Plan: Core (39€/mois) ou Pro (99€/mois si > 10K ops)

#### 4.2 Workflows à créer

**Workflow 1: Bank Connection**
- Trigger: Webhook from Bubble
- Action: Bridge API - Generate connect URL
- Action: Return to Bubble

**Workflow 2: Sync Transactions (Daily)**
- Trigger: Schedule (6:00 AM daily)
- Action: Get all bank accounts (Supabase)
- Loop: For each account
  - Action: Bridge API - Get transactions
  - Action: Claude API - Categorize
  - Action: Insert Supabase
  - Action: Check reconciliation

**Workflow 3: Auto-Reconciliation**
- Trigger: New transaction webhook
- Action: Get unpaid invoices
- Action: Matching algorithm
- Action: Claude API - Fuzzy match
- Condition: If score > 0.80 → Auto validate
- Action: Update Supabase

**Workflow 4: Send Reminders**
- Trigger: Schedule (Monday 9 AM)
- Action: Get overdue invoices
- Loop: For each invoice
  - Action: Claude API - Generate email
  - Action: SendGrid - Send email
  - Action: Log reminder

#### 4.3 Webhooks Configuration

Dans Bubble, API Connector:
- POST /make/bank-connect
- POST /make/trigger-sync
- POST /make/new-transaction

---

### Étape 5: Premier Workflow (Semaine 3-4)

**Test complet Banking Integration**:

1. **Dans Bubble**: Créer bouton "Connecter ma banque"
2. **Workflow Bubble**:
   - Send data to external API (Make webhook)
   - user_id → Make

3. **Dans Make**:
   - Receive webhook
   - Bridge API: Generate connect URL
   - HTTP Response back to Bubble

4. **Dans Bubble**:
   - Afficher URL Bridge dans popup
   - User complète OAuth
   - Bridge webhook → Make
   - Make → Store account Supabase

5. **Test**:
   - User connecte compte sandbox Bridge
   - Transactions apparaissent dans Supabase
   - Catégorisation IA fonctionne

---

### Étape 6: Beta Launch (Semaine 7-8)

**Checklist avant lancement beta**:

- [ ] 5 features core fonctionnelles:
  - [ ] Connexion bancaire
  - [ ] Sync transactions
  - [ ] Import factures
  - [ ] Rapprochements auto
  - [ ] Relances emails

- [ ] Tests manuels complets
- [ ] 3 comptes bancaires différents testés
- [ ] 50 transactions test (90%+ catégorisation correcte)
- [ ] 20 rapprochements test (90%+ matching correct)
- [ ] 10 emails relances générés (qualité vérifiée)

- [ ] Documentation utilisateur basique
- [ ] Onboarding flow créé
- [ ] Support email setup (support@financeai.fr)

- [ ] CGU/CGV rédigées
- [ ] Politique confidentialité (RGPD)
- [ ] Mentions légales

**Inviter beta users** (5-10 pre-sales):
```
Sujet: 🎉 Bienvenue dans la beta FinanceAI!

Bonjour [Prénom],

Merci d'avoir rejoint la beta FinanceAI en tant que client fondateur!

Votre accès est maintenant activé:
👉 https://financeai.bubble.io/dashboard

Prix garanti lifetime: 199€/mois (vs 399€ futur)

Vos prochaines étapes:
1. Connecter votre compte bancaire
2. Importer vos factures (CSV ou manuel)
3. Laisser la magie opérer ✨

Questions? Répondez à cet email, je réponds sous 2h.

Yves
Founder, FinanceAI
```

---

## Phase 2: Migration Code (Semaines 9-20)

**Trigger migration**:
- 30+ clients actifs
- MRR > 15K€
- Feedback: features limitées no-code

**Setup voir**: `backend/README.md` et `frontend/README.md` (à créer)

---

## 📊 Métriques à Tracker

**Dashboard (Google Sheets ou Notion)**:

| Métrique | Cible Semaine 8 | Actuel |
|----------|----------------|--------|
| Clients beta | 20-30 | 0 |
| MRR | 4K-6K€ | 0€ |
| NPS | > 40 | - |
| Churn | < 5% | - |
| Précision réconciliations | > 90% | - |
| Bugs critiques | < 10 | 0 |
| Temps réponse support | < 4h | - |

---

## 🆘 Support & Resources

**Documentation**:
- Bubble: https://manual.bubble.io
- Make: https://www.make.com/en/help
- Bridge API: https://docs.bridgeapi.io
- Claude API: https://docs.anthropic.com
- Supabase: https://supabase.com/docs

**Communautés**:
- Bubble Forum: https://forum.bubble.io
- Make Community: https://community.make.com
- Discord FinTech France (chercher sur Google)

**Contact**:
- Questions roadmap: Voir ROADMAP_FINANCE_PME.md
- Questions code (Phase 2): Voir .cursorrules

---

## ⚠️ Important - Sécurité

**JAMAIS commit**:
- `.env` files
- API keys
- Secrets
- Données clients

**TOUJOURS**:
- Tester en sandbox d'abord
- Sauvegarder database quotidiennement
- Valider inputs utilisateurs
- Logs sans données sensibles

---

## 🎯 Next Steps Immédiats

### Cette semaine:
1. [ ] Créer comptes (Bubble, Make, Supabase, Bridge, Claude)
2. [ ] Setup database Supabase
3. [ ] Test Bridge API sandbox
4. [ ] Test Claude API categorization
5. [ ] Premier workflow Make.com

### Semaine prochaine:
1. [ ] Pages Bubble (dashboard, transactions, invoices)
2. [ ] Workflow sync complet
3. [ ] Tests manuels approfondis
4. [ ] Inviter 1er beta user

---

**Prêt à coder? Let's go! 🚀**

