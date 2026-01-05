# 🔥 PLAN DE DÉVELOPPEMENT IMMÉDIAT - FinanceAI

## ✅ VALIDATION CONFIRMÉE - ON FONCE !

**Date démarrage**: Maintenant
**Objectif**: MVP fonctionnel avec premiers clients sous **6 semaines**
**Budget dev**: 2,000€

---

## 🎯 SEMAINES 1-2: FOUNDATION (Setup + Banking)

### JOUR 1 - AUJOURD'HUI : Setup Comptes (4 heures)

#### Bloc 1: Supabase (30 min)
```bash
✅ ACTIONS IMMÉDIATES:
1. https://supabase.com → Sign up
2. New Project: "financeai-prod"
3. Region: Europe West (Frankfurt)
4. Password: [générer avec: openssl rand -base64 32]
5. Attendre 2 min (provisioning)

6. SQL Editor:
   - Copier TOUT le contenu de database_schema.sql
   - Paste dans SQL Editor
   - Run (⌘/Ctrl + Enter)
   - Vérifier: Tables (sidebar) → 8 tables visibles ✅

7. Project Settings → API:
   - Copier: Project URL
   - Copier: anon public key
   - Copier: service_role key (secret!)
   
8. Database → Connection string:
   - Copier: postgres://postgres:[PASSWORD]@...
```

#### Bloc 2: Bridge API (30 min)
```bash
✅ ACTIONS:
1. https://dashboard.bridgeapi.io/signup
2. Email + Password
3. Verify email
4. Create application: "FinanceAI Production"
5. Environment: SANDBOX (pour tests)

6. Dashboard → Credentials:
   - Client ID: [copier]
   - Client Secret: [copier]
   - API Key: [copier]

7. TEST IMMÉDIAT:
curl -X POST https://api.bridgeapi.io/v2/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_EMAIL",
    "password": "YOUR_PASSWORD"
  }'

# Doit retourner: {"access_token": "...", "expires_at": "..."}
# ✅ = API fonctionne
```

#### Bloc 3: Anthropic Claude (15 min)
```bash
✅ ACTIONS:
1. https://console.anthropic.com/signup
2. Verify email
3. Settings → API Keys → Create Key
4. Name: "FinanceAI Production"
5. Copier la clé (commence par sk-ant-...)

6. TEST IMMÉDIAT:
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user", 
        "content": "Categorize: VIR LOYER BUREAU JANVIER - 1500 EUR. Return JSON: {category: string, confidence: number}"
      }
    ]
  }'

# Doit retourner JSON avec catégorie
# ✅ = IA fonctionne
```

#### Bloc 4: SendGrid (20 min)
```bash
✅ ACTIONS:
1. https://signup.sendgrid.com
2. Free plan (100 emails/jour - suffisant pour MVP)
3. Complete setup wizard
4. Settings → API Keys → Create API Key
5. Name: "FinanceAI Production"
6. Permissions: Full Access
7. Copier la clé (SG.xxxx)

8. Sender Authentication → Single Sender Verification:
   - From Email: noreply@financeai.fr
   - From Name: FinanceAI
   - Verify email

9. TEST (après vérification):
curl -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{
      "to": [{"email": "YOUR_EMAIL"}]
    }],
    "from": {"email": "noreply@financeai.fr"},
    "subject": "Test FinanceAI",
    "content": [{
      "type": "text/plain",
      "value": "Email system works!"
    }]
  }'

# Check votre inbox
# ✅ = Emails fonctionnent
```

#### Bloc 5: Stripe (20 min)
```bash
✅ ACTIONS:
1. https://dashboard.stripe.com/register
2. Complete business info
3. Activate test mode (toggle top-right)

4. Developers → API Keys (Test mode):
   - Publishable key: pk_test_xxx [copier]
   - Secret key: sk_test_xxx [copier]

5. Products → Add product:
   
   PRODUCT 1:
   - Name: FinanceAI Starter
   - Description: 1 compte bancaire, 100 factures/mois
   - Price: 399€/month
   - Recurring
   - [Save] → Copier Price ID

   PRODUCT 2:
   - Name: FinanceAI Pro
   - Description: 3 comptes, 500 factures/mois
   - Price: 699€/month
   - [Save] → Copier Price ID

   PRODUCT 3:
   - Name: FinanceAI Business
   - Description: Illimité
   - Price: 999€/month
   - [Save] → Copier Price ID

6. Webhooks → Add endpoint:
   - URL: https://financeai.bubbleapps.io/api/1.1/wf/stripe-webhook
   - Events: customer.subscription.created, updated, deleted
   - [Add endpoint] → Copier Signing secret
```

#### Bloc 6: Bubble.io (30 min)
```bash
✅ ACTIONS:
1. https://bubble.io/build
2. New app → Start from scratch
3. App name: "FinanceAI"
4. Plan: Starter (29€/mois) - PAYER MAINTENANT

5. Settings → General:
   - App name: FinanceAI
   - App description: Automatisation comptable PME

6. Settings → Domain / email:
   - Domain: financeai.bubbleapps.io (default OK pour MVP)
   - Custom domain: [plus tard]

7. Settings → API:
   - Enable API
   - Enable workflows
   - Generate API token → [copier]

8. NE PAS FERMER - on va créer la structure juste après
```

#### Bloc 7: Make.com (30 min)
```bash
✅ ACTIONS:
1. https://www.make.com/en/register
2. Organization name: FinanceAI
3. Plan: Core (39€/mois) - PAYER MAINTENANT

4. Create Team: "FinanceAI Team"

5. Create Scenarios (vides pour l'instant):
   - Scenario 1: "Bank Connection Flow"
   - Scenario 2: "Daily Sync Transactions"  
   - Scenario 3: "Auto Reconciliation"
   - Scenario 4: "Send Reminders"

6. Pour chaque scenario:
   - Settings → Webhook
   - Copier webhook URL (https://hook.eu1.make.com/xxx)

7. NE PAS FERMER - on va les configurer après
```

#### Bloc 8: Configuration .env (15 min)
```bash
✅ ACTIONS:
cd ~/Documents/Projet  # (ou votre path)
cp env.template .env
code .env  # ou vim, nano

# Remplir TOUTES les valeurs copiées ci-dessus:
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOi...
DATABASE_URL=postgresql://postgres:...

BRIDGE_ENV=sandbox
BRIDGE_CLIENT_ID=xxx
BRIDGE_CLIENT_SECRET=xxx
BRIDGE_API_KEY=xxx

ANTHROPIC_API_KEY=sk-ant-xxx

SENDGRID_API_KEY=SG.xxx
SENDGRID_FROM_EMAIL=noreply@financeai.fr

STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PRICE_STARTER=price_xxx
STRIPE_PRICE_PRO=price_xxx
STRIPE_PRICE_BUSINESS=price_xxx

BUBBLE_APP_URL=https://financeai.bubbleapps.io
BUBBLE_API_KEY=xxx

MAKE_WEBHOOK_BANK_CONNECT=https://hook.eu1.make.com/xxx
MAKE_WEBHOOK_SYNC=https://hook.eu1.make.com/xxx
MAKE_WEBHOOK_RECONCILE=https://hook.eu1.make.com/xxx
MAKE_WEBHOOK_REMINDERS=https://hook.eu1.make.com/xxx

# Save & close
```

#### ✅ CHECKPOINT JOUR 1 (Fin de journée)

**Vérifications**:
- [ ] Supabase: 8 tables créées ✅
- [ ] Bridge API: curl test fonctionne ✅
- [ ] Claude API: catégorisation test OK ✅
- [ ] SendGrid: email test reçu ✅
- [ ] Stripe: 3 produits créés ✅
- [ ] Bubble.io: App créée ✅
- [ ] Make.com: 4 scenarios créés ✅
- [ ] .env: Toutes les variables remplies ✅

**Commit Git**:
```bash
git add .env
git commit -m "chore: Configure environment variables (DO NOT PUSH)"
# NE PAS PUSH .env !!
```

**État**: Infrastructure 100% prête → Peut commencer dev features

---

## JOUR 2-3: Bubble.io - Structure App (8 heures)

### Data Types (1 heure)

Dans Bubble.io → Data → Data types:

```
1. User (modifier le type existant):
   Fields:
   - email (email) [already exists]
   - company_name (text)
   - company_size (text): Options list [1-10, 10-50, 50-200, 200+]
   - subscription_plan (text): Options list [trial, starter, pro, business]
   - subscription_status (text): Options list [active, cancelled, expired]
   - stripe_customer_id (text)
   - supabase_user_id (text)

2. BankAccount (créer):
   Fields:
   - user (User)
   - bridge_account_id (text)
   - bank_name (text)
   - account_type (text)
   - iban (text)
   - balance (number)
   - currency (text): Default value "EUR"
   - is_active (yes/no): Default value yes
   - last_sync_at (date)

3. Transaction (créer):
   Fields:
   - bank_account (BankAccount)
   - bridge_transaction_id (text)
   - date (date)
   - description (text)
   - amount (number)
   - category (text)
   - category_confidence (number)
   - is_reconciled (yes/no): Default value no
   - reconciliation (Reconciliation) [optional]

4. Invoice (créer):
   Fields:
   - user (User)
   - invoice_number (text)
   - client_name (text)
   - client_email (email)
   - amount (number)
   - issue_date (date)
   - due_date (date)
   - status (text): Options list [pending, paid, overdue, cancelled]
   - payment_date (date) [optional]
   - is_reconciled (yes/no): Default value no
   - reconciliation (Reconciliation) [optional]
   - notes (text) [optional]

5. Reconciliation (créer):
   Fields:
   - user (User)
   - transaction (Transaction)
   - invoice (Invoice)
   - match_score (number): Min 0, Max 1
   - match_method (text): Options list [exact, reference, fuzzy_ai, manual]
   - validated_by (text): Options list [ai, user]
   - validated_at (date)
   - notes (text) [optional]

6. Reminder (créer):
   Fields:
   - invoice (Invoice)
   - sent_at (date)
   - reminder_type (text): Options list [first, second, final]
   - email_subject (text)
   - email_body (text)
   - opened_at (date) [optional]
   - clicked_at (date) [optional]
   - status (text): Options list [sent, opened, clicked, replied]
```

**Privacy Rules** (IMPORTANT - Sécurité):
```
Pour CHAQUE data type:
1. View all: Current User's xxx (field user = Current User)
2. Auto-bind: user = Current User
3. Create/Modify/Delete: Current User's xxx

Exemple pour Invoice:
- View: This Invoice's user is Current User
- Create: This Invoice's user is Current User
- Modify: This Invoice's user is Current User
- Delete: This Invoice's user is Current User
```

### Pages Structure (2 heures)

**Créer ces pages** dans Bubble:

```
1. index (Homepage - Not logged in)
   - Header: Logo, "Se connecter", "Démarrer"
   - Hero section
   - CTA: "Commencer gratuitement"
   - Footer

2. login
   - Email + Password fields
   - "Se connecter" button
   - Link: "Créer un compte"
   - Link: "Mot de passe oublié"

3. signup
   - Email, Password, Confirm password
   - Company name
   - Company size (dropdown)
   - "Créer mon compte" button
   - Link: "J'ai déjà un compte"

4. dashboard (Homepage - Logged in)
   - Sidebar navigation
   - Header: User email, "Déconnexion"
   - Main content area:
     * KPIs (4 boxes):
       - Solde total
       - Factures en attente
       - Trésorerie prévue
       - Réconciliations à valider
     * Chart: Évolution trésorerie
     * Recent activity list

5. bank-accounts
   - List of bank accounts (Repeating Group)
   - Button: "Connecter une banque"
   - For each: Bank name, IBAN, Balance, Last sync
   - Button: "Synchroniser maintenant"

6. transactions
   - Filters: Date range, Category, Reconciled yes/no
   - Repeating Group: Transactions list
   - Columns: Date, Description, Amount, Category, Status
   - Click row → Transaction detail popup

7. invoices
   - Button: "Nouvelle facture"
   - Button: "Importer CSV"
   - Repeating Group: Invoices list
   - Columns: Number, Client, Amount, Due date, Status
   - Click row → Invoice detail popup

8. reconciliations
   - Pending reconciliations (match_score > 0.5, not validated)
   - For each: Transaction + Suggested invoice + Score
   - Buttons: "Valider", "Rejeter"

9. settings
   - Tabs: Account, Subscription, Billing
   - Account: Company info, Email
   - Subscription: Current plan, Upgrade button
   - Billing: Stripe customer portal link
```

### Reusable Elements (1 heure)

```
1. Sidebar Navigation:
   - Links: Dashboard, Transactions, Invoices, Reconciliations, Bank Accounts, Settings
   - Active state styling
   - User info at bottom

2. KPI Card:
   - Title (text)
   - Value (text/number)
   - Icon
   - Change % (optional)

3. Transaction Row:
   - Date, Description, Amount, Category
   - Reconciled badge (if yes)

4. Invoice Row:
   - Invoice number, Client, Amount, Due date
   - Status badge (pending/paid/overdue)

5. Loading Spinner:
   - Show when API call in progress

6. Toast Notification:
   - Success / Error message
   - Auto-hide after 3s
```

### Workflows Bubble (2 heures)

**Workflow 1: User Sign Up**
```
Trigger: Button "Créer mon compte" is clicked

Steps:
1. Sign the user up
   - Email: Input Email's value
   - Password: Input Password's value

2. Create a new User (if not auto-created)
   - email: Result of step 1's email
   - company_name: Input Company name's value
   - company_size: Dropdown Company size's value
   - subscription_plan: "trial"
   - subscription_status: "active"

3. Create a new thing in Supabase (via API Connector)
   - Table: users
   - Data: Current User's fields

4. Navigate to: dashboard
```

**Workflow 2: User Login**
```
Trigger: Button "Se connecter" is clicked

Steps:
1. Log the user in
   - Email: Input Email's value
   - Password: Input Password's value

2. Navigate to: dashboard
```

**Workflow 3: Connect Bank Account**
```
Trigger: Button "Connecter une banque" is clicked

Steps:
1. Call Make.com webhook (Bank Connection Flow)
   - POST to: MAKE_WEBHOOK_BANK_CONNECT
   - Body: {"user_id": Current User's id}

2. Display Result of step 1 in popup
   - Show: Bridge connect URL in iframe

3. When webhook receives "success" callback:
   - Create new BankAccount
   - Refresh Repeating Group
```

**Workflow 4: Sync Transactions**
```
Trigger: Button "Synchroniser maintenant" is clicked

Steps:
1. Set state "is_loading" = yes

2. Call Make.com webhook (Daily Sync)
   - POST to: MAKE_WEBHOOK_SYNC
   - Body: {"bank_account_id": This BankAccount's id}

3. Wait for result (polling every 2s, max 30s)

4. Set state "is_loading" = no

5. Show notification: "X transactions synchronisées"

6. Refresh Repeating Group
```

**Workflow 5: Create Invoice**
```
Trigger: Button "Créer la facture" is clicked (in popup)

Steps:
1. Create a new Invoice
   - user: Current User
   - invoice_number: Input Number's value
   - client_name: Input Client's value
   - amount: Input Amount's value
   - due_date: Input Due date's value
   - status: "pending"

2. Create in Supabase (API)

3. Close popup

4. Show notification: "Facture créée"

5. Reset inputs

6. Refresh Repeating Group
```

**Workflow 6: Validate Reconciliation**
```
Trigger: Button "Valider" is clicked (on reconciliation suggestion)

Steps:
1. Make changes to This Reconciliation
   - validated_by: "user"
   - validated_at: Current date/time

2. Make changes to This Reconciliation's transaction
   - is_reconciled: yes
   - reconciliation: This Reconciliation

3. Make changes to This Reconciliation's invoice
   - is_reconciled: yes
   - status: "paid"
   - payment_date: This Reconciliation's transaction's date
   - reconciliation: This Reconciliation

4. Update Supabase (API)

5. Show notification: "Rapprochement validé"

6. Remove from Repeating Group
```

### API Connector Setup (2 heures)

**API 1: Supabase**
```
Name: Supabase
Type: Private (API key in header)
Authentication: Self-handled

Base URL: https://YOUR_PROJECT.supabase.co/rest/v1

Headers:
- apikey: YOUR_SUPABASE_ANON_KEY
- Authorization: Bearer YOUR_SUPABASE_ANON_KEY
- Content-Type: application/json
- Prefer: return=representation

Calls:

1. Get Users
   - Type: GET
   - Path: /users?id=eq.[id]
   - [id]: Dynamic (text)

2. Create User
   - Type: POST
   - Path: /users
   - Body: {"email": "[email]", "company_name": "[company]", ...}

3. Get Transactions
   - Type: GET
   - Path: /transactions?bank_account_id=eq.[account_id]&order=date.desc
   - [account_id]: Dynamic

4. Create Transaction
   - Type: POST
   - Path: /transactions
   - Body: Transaction JSON

5. Get Invoices
   - Type: GET
   - Path: /invoices?user_id=eq.[user_id]&order=due_date.asc
   - [user_id]: Dynamic

... (etc pour toutes les tables)
```

**API 2: Make.com Webhooks**
```
Name: Make_Webhooks
Type: Private
Authentication: None (webhook security via secret)

Calls:

1. Trigger_Bank_Connect
   - Type: POST
   - URL: YOUR_MAKE_WEBHOOK_URL_1
   - Body: {"user_id": "[user_id]"}

2. Trigger_Sync
   - Type: POST
   - URL: YOUR_MAKE_WEBHOOK_URL_2
   - Body: {"bank_account_id": "[account_id]"}

3. Trigger_Reconcile
   - Type: POST  
   - URL: YOUR_MAKE_WEBHOOK_URL_3
   - Body: {"transaction_id": "[transaction_id]"}

4. Trigger_Reminders
   - Type: POST
   - URL: YOUR_MAKE_WEBHOOK_URL_4
   - Body: {"user_id": "[user_id]"}
```

### ✅ CHECKPOINT JOUR 2-3

**Vérifications**:
- [ ] 6 Data types créés avec tous les fields ✅
- [ ] Privacy rules configurées (sécurité) ✅
- [ ] 9 pages créées avec structure ✅
- [ ] 5 reusable elements créés ✅
- [ ] 6 workflows principaux créés ✅
- [ ] 2 API connectors configurés ✅

**Test manuel**:
- [ ] Signup → Login → Dashboard (affiche) ✅
- [ ] Navigation sidebar fonctionne ✅
- [ ] Pages se chargent sans erreur ✅

**Commit Git**:
```bash
git add docs/bubble-structure.md  # documenter ce qui a été fait
git commit -m "feat: Complete Bubble.io app structure"
git push
```

---

## JOUR 4-5: Make.com Workflows (8 heures)

**Suite dans le prochain fichier**: `MAKE_WORKFLOWS_SETUP.md`

---

## MÉTRIQUES SUCCÈS SEMAINE 1-2

- [ ] Infrastructure 100% opérationnelle
- [ ] Bubble.io: Structure complète + navigable
- [ ] Make.com: 2 workflows fonctionnels (Bank + Sync)
- [ ] Premier test end-to-end: Connexion banque → Transactions affichées
- [ ] 0 bugs bloquants

---

**FOCUS**: Exécution rapide, pas de perfectionnisme. MVP = Minimum Viable Product.

**ON Y VA! 🚀**

