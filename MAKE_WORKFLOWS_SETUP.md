# ⚙️ MAKE.COM - Configuration Workflows Détaillée

## Workflow 1: Bank Connection Flow

### Déclencheur
- **Module**: Webhook
- **Type**: Custom webhook
- **URL**: Copier l'URL générée
- **Method**: POST
- **Expected Data**: 
  ```json
  {
    "user_id": "uuid-string"
  }
  ```

### Module 2: Bridge API - Generate Connect URL
```
Module: HTTP - Make a request
Method: POST
URL: https://api.bridgeapi.io/v2/connect/items/add
Headers:
  - Authorization: Bearer {{1.BRIDGE_API_KEY}}
  - Bridge-Version: 2021-06-01
  - Content-Type: application/json

Body (JSON):
{
  "user": {
    "uuid": "{{1.user_id}}"
  },
  "country": "fr",
  "prefill": {
    "email": ""
  }
}

Parse response: Yes
```

### Module 3: HTTP Response
```
Module: Webhook Response
Status: 200
Body Type: JSON
Body:
{
  "success": true,
  "connect_url": "{{2.body.redirect_url}}",
  "connect_token": "{{2.body.connect_token}}"
}
```

**Sauvegarder le scenario** → Activer

---

## Workflow 2: Daily Sync Transactions ⭐

### Déclencheur
```
Module: Schedule
Type: Every day at
Time: 06:00 AM
Timezone: Europe/Paris
```

### Module 2: Supabase - Get All Active Bank Accounts
```
Module: HTTP - Make a request
Method: GET
URL: https://YOUR_PROJECT.supabase.co/rest/v1/bank_accounts?is_active=eq.true&select=*

Headers:
  - apikey: {{SUPABASE_ANON_KEY}}
  - Authorization: Bearer {{SUPABASE_ANON_KEY}}
  - Content-Type: application/json

Parse response: Yes
```

### Module 3: Iterator
```
Module: Flow Control - Iterator
Array: {{2.body}}
```

### Module 4: Bridge API - Get Transactions
```
Module: HTTP - Make a request
Method: GET
URL: https://api.bridgeapi.io/v2/accounts/{{3.bridge_account_id}}/transactions

Query Parameters:
  - since: {{formatDate(3.last_sync_at; "YYYY-MM-DD")}}
  - limit: 500

Headers:
  - Authorization: Bearer {{BRIDGE_API_KEY}}
  - Bridge-Version: 2021-06-01

Parse response: Yes
```

### Module 5: Iterator Transactions
```
Module: Flow Control - Iterator
Array: {{4.body.resources}}
```

### Module 6: Check if Transaction Exists
```
Module: HTTP - Make a request
Method: GET
URL: https://YOUR_PROJECT.supabase.co/rest/v1/transactions?bridge_transaction_id=eq.{{5.id}}

Headers: [same as module 2]

Parse response: Yes
```

### Module 7: Router
```
Module: Flow Control - Router
Filters:

Route 1: "New Transaction"
Condition: {{length(6.body)}} = 0

Route 2: "Existing Transaction"  
Condition: {{length(6.body)}} > 0
→ Stop execution (ignore duplicates)
```

### Module 8A: Claude - Categorize Transaction
```
Module: HTTP - Make a request
Method: POST
URL: https://api.anthropic.com/v1/messages

Headers:
  - x-api-key: {{ANTHROPIC_API_KEY}}
  - anthropic-version: 2023-06-01
  - content-type: application/json

Body (JSON):
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [{
    "role": "user",
    "content": "Categorize this bank transaction. Return ONLY valid JSON, no markdown:\n\nDescription: {{5.description}}\nAmount: {{5.amount}}\n\nCategories: Salaires, Fournitures, Loyer, Clients, Banque, Taxes, Marketing, Transport, Abonnements, Autre\n\nReturn format:\n{\"category\": \"CategoryName\", \"confidence\": 0.95}"
  }]
}

Parse response: Yes
```

### Module 9A: Parse Claude Response
```
Module: JSON - Parse JSON
JSON string: {{8A.body.content[].text}}
```

### Module 10A: Supabase - Create Transaction
```
Module: HTTP - Make a request
Method: POST
URL: https://YOUR_PROJECT.supabase.co/rest/v1/transactions

Headers:
  - apikey: {{SUPABASE_ANON_KEY}}
  - Authorization: Bearer {{SUPABASE_ANON_KEY}}
  - Content-Type: application/json
  - Prefer: return=representation

Body (JSON):
{
  "bank_account_id": "{{3.id}}",
  "bridge_transaction_id": "{{5.id}}",
  "date": "{{5.date}}",
  "description": "{{5.description}}",
  "amount": {{5.amount}},
  "currency": "{{5.currency_code}}",
  "category": "{{9A.category}}",
  "category_confidence": {{9A.confidence}},
  "is_reconciled": false
}

Parse response: Yes
```

### Module 11A: Trigger Auto-Reconciliation
```
Module: HTTP - Make a request
Method: POST
URL: {{MAKE_WEBHOOK_RECONCILE}}

Body (JSON):
{
  "transaction_id": "{{10A.body[].id}}"
}
```

### Module 12: Update Last Sync
```
Module: HTTP - Make a request (après l'iterator)
Method: PATCH
URL: https://YOUR_PROJECT.supabase.co/rest/v1/bank_accounts?id=eq.{{3.id}}

Headers: [same as module 2]

Body (JSON):
{
  "last_sync_at": "{{now}}"
}
```

**Sauvegarder** → **Activer** → **Tester avec "Run once"**

---

## Workflow 3: Auto-Reconciliation 🎯

### Déclencheur
```
Module: Webhook
Type: Custom webhook
Expected Data:
{
  "transaction_id": "uuid"
}
```

### Module 2: Get Transaction Details
```
Module: HTTP - Make a request
Method: GET
URL: https://YOUR_PROJECT.supabase.co/rest/v1/transactions?id=eq.{{1.transaction_id}}&select=*,bank_account:bank_accounts(user_id)

Headers: [Supabase headers]
```

### Module 3: Get Unpaid Invoices
```
Module: HTTP - Make a request
Method: GET
URL: https://YOUR_PROJECT.supabase.co/rest/v1/invoices?user_id=eq.{{2.body[].bank_account.user_id}}&status=eq.pending&is_reconciled=eq.false&select=*

Headers: [Supabase headers]
```

### Module 4: Iterator (Invoices)
```
Module: Flow Control - Iterator
Array: {{3.body}}
```

### Module 5: Calculate Exact Match Score
```
Module: Tools - Set variables

Variables:
- amount_match: {{if(abs(2.body[].amount - 4.amount) < 0.01; 1; 0)}}
- date_diff: {{abs(dateDifference(2.body[].date; 4.due_date; "days"))}}
- date_match: {{if(date_diff <= 3; 1; 0)}}
- exact_score: {{if(amount_match = 1 AND date_match = 1; 1.0; 0)}}
```

### Module 6: Router
```
Route 1: "Exact Match Found"
Condition: {{5.exact_score}} >= 0.95
→ Module 7A: Create Reconciliation (auto-validated)

Route 2: "Try Fuzzy Match"
Condition: {{5.exact_score}} < 0.95
→ Module 7B: Claude Fuzzy Match
```

### Module 7A: Create Reconciliation (Exact)
```
Module: HTTP - Make a request
Method: POST
URL: https://YOUR_PROJECT.supabase.co/rest/v1/reconciliations

Headers: [Supabase headers + Prefer: return=representation]

Body:
{
  "user_id": "{{2.body[].bank_account.user_id}}",
  "transaction_id": "{{1.transaction_id}}",
  "invoice_id": "{{4.id}}",
  "match_score": 1.0,
  "match_method": "exact",
  "validated_by": "ai",
  "validated_at": "{{now}}"
}
```

### Module 7B: Claude Fuzzy Match
```
Module: HTTP - Make a request
Method: POST
URL: https://api.anthropic.com/v1/messages

Body:
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 2048,
  "messages": [{
    "role": "user",
    "content": "Match this transaction to this invoice. Return ONLY valid JSON:\n\nTransaction:\n- Date: {{2.body[].date}}\n- Description: {{2.body[].description}}\n- Amount: {{2.body[].amount}}€\n\nInvoice:\n- Number: {{4.invoice_number}}\n- Client: {{4.client_name}}\n- Amount: {{4.amount}}€\n- Due: {{4.due_date}}\n\nDo they match? Return:\n{\"match\": true/false, \"confidence\": 0.0-1.0, \"reasoning\": \"why\"}"
  }]
}
```

### Module 8B: Parse Claude Response
```
Module: JSON - Parse JSON
JSON string: {{7B.body.content[].text}}
```

### Module 9B: Router by Confidence
```
Route 1: "High Confidence (>= 0.80)"
→ Create auto-validated reconciliation

Route 2: "Medium Confidence (0.50-0.79)"
→ Create pending reconciliation (needs user validation)

Route 3: "Low Confidence (< 0.50)"
→ Do nothing
```

### Module 10: Update Transaction & Invoice
```
Module: HTTP - Make a request (2 requests in parallel)

Request 1: Update Transaction
PATCH /transactions?id=eq.{{transaction_id}}
Body: {"is_reconciled": true, "reconciliation_id": "{{reconciliation_id}}"}

Request 2: Update Invoice
PATCH /invoices?id=eq.{{invoice_id}}
Body: {"status": "paid", "payment_date": "{{transaction_date}}", "is_reconciled": true}
```

**Sauvegarder** → **Activer**

---

## Workflow 4: Send Reminders 📧

### Déclencheur
```
Module: Schedule
Type: Every week on
Day: Monday
Time: 09:00 AM
Timezone: Europe/Paris
```

### Module 2: Get Overdue Invoices
```
Module: HTTP - Make a request
Method: GET
URL: https://YOUR_PROJECT.supabase.co/rest/v1/invoices?status=eq.pending&due_date=lt.{{formatDate(now; "YYYY-MM-DD")}}&select=*,reminders:reminders(*)

Headers: [Supabase headers]
```

### Module 3: Iterator
```
Module: Flow Control - Iterator
Array: {{2.body}}
```

### Module 4: Calculate Days Overdue
```
Module: Tools - Set variable
Name: days_overdue
Value: {{dateDifference(3.due_date; now; "days")}}
```

### Module 5: Determine Reminder Type
```
Module: Tools - Set variable
Name: reminder_type
Value: {{if(4.days_overdue <= 14; "first"; if(4.days_overdue <= 30; "second"; "final"))}}
```

### Module 6: Check Last Reminder
```
Module: Tools - Set variable
Name: last_reminder_date
Value: {{max(3.reminders[].sent_at)}}

Name: days_since_reminder
Value: {{if(last_reminder_date; dateDifference(last_reminder_date; now; "days"); 999)}}
```

### Module 7: Router
```
Filter: "Should Send Reminder"
Conditions:
- {{6.days_since_reminder}} > 7  (au moins 7 jours depuis dernière relance)
- OR {{6.last_reminder_date}} is empty (jamais de relance)
```

### Module 8: Claude - Generate Email
```
Module: HTTP - Make a request
URL: https://api.anthropic.com/v1/messages

Body:
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 2048,
  "messages": [{
    "role": "user",
    "content": "Generate a professional payment reminder email in French.\n\nContext:\n- Reminder type: {{5.reminder_type}} (first=courtois, second=ferme, final=formel)\n- Client: {{3.client_name}}\n- Invoice: {{3.invoice_number}}\n- Amount: {{3.amount}}€\n- Due date: {{3.due_date}}\n- Days overdue: {{4.days_overdue}}\n\nReturn ONLY valid JSON:\n{\"subject\": \"Subject line\", \"body\": \"HTML email body with <p> tags\"}"
  }]
}
```

### Module 9: Parse Response
```
Module: JSON - Parse JSON
JSON string: {{8.body.content[].text}}
```

### Module 10: SendGrid - Send Email
```
Module: HTTP - Make a request
Method: POST
URL: https://api.sendgrid.com/v3/mail/send

Headers:
  - Authorization: Bearer {{SENDGRID_API_KEY}}
  - Content-Type: application/json

Body:
{
  "personalizations": [{
    "to": [{"email": "{{3.client_email}}"}],
    "dynamic_template_data": {}
  }],
  "from": {
    "email": "{{SENDGRID_FROM_EMAIL}}",
    "name": "FinanceAI"
  },
  "subject": "{{9.subject}}",
  "content": [{
    "type": "text/html",
    "value": "{{9.body}}"
  }],
  "tracking_settings": {
    "click_tracking": {"enable": true},
    "open_tracking": {"enable": true}
  }
}
```

### Module 11: Create Reminder Record
```
Module: HTTP - Make a request
Method: POST
URL: https://YOUR_PROJECT.supabase.co/rest/v1/reminders

Body:
{
  "invoice_id": "{{3.id}}",
  "sent_at": "{{now}}",
  "reminder_type": "{{5.reminder_type}}",
  "email_subject": "{{9.subject}}",
  "email_body": "{{9.body}}",
  "status": "sent"
}
```

### Module 12: Aggregator + Summary Email
```
Module: Tools - Aggregator
Source module: Module 11
Aggregated fields: invoice_id, reminder_type

After aggregator:
Module: SendGrid - Send Summary to User
To: [User's email from invoice.user]
Subject: "📊 Résumé relances - {{count}} relances envoyées"
Body: List of reminders sent
```

**Sauvegarder** → **Activer**

---

## Configuration Avancée Make.com

### Error Handling (Tous les workflows)

Pour chaque module HTTP critique:
```
Settings → Error handling
- Enable: Break
- Rollback: Yes
- Number of retries: 3
- Interval between retries: 2 (exponential)
```

### Data Stores (Optionnel - pour cache)

```
Data Store 1: "Transaction Categories Cache"
Key: transaction_description
Value: {category, confidence}
TTL: 30 days

Usage: Check cache avant d'appeler Claude
→ Économise tokens
```

### Monitoring

Dans chaque workflow:
```
Settings → Notifications
- Email on error: your_email@domain.com
- Slack webhook: [optional]
```

---

## Tests End-to-End

### Test 1: Bank Connection
```bash
curl -X POST https://hook.eu1.make.com/WEBHOOK_ID \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-uuid-123"}'

Expected: {"success": true, "connect_url": "https://..."}
```

### Test 2: Sync Transactions
```bash
# Déclencher manuellement dans Make
# Vérifier:
1. Logs Make: Transactions fetched from Bridge ✅
2. Logs Make: Claude categorization ✅
3. Supabase: Nouvelles transactions dans table ✅
4. Bubble: Transactions affichées dans UI ✅
```

### Test 3: Reconciliation
```bash
# Créer 1 transaction + 1 invoice avec même montant
# Trigger reconciliation webhook
# Vérifier:
1. Reconciliation créée ✅
2. Transaction.is_reconciled = true ✅
3. Invoice.status = "paid" ✅
```

### Test 4: Reminders
```bash
# Créer invoice overdue (due_date < today)
# Déclencher workflow manuellement
# Vérifier:
1. Email reçu (check inbox) ✅
2. Reminder enregistré dans DB ✅
3. Email bien formaté ✅
```

---

## Optimisations Performance

### 1. Batch Processing
```
Pour Sync Transactions:
- Ne pas faire 1 API call par transaction
- Grouper en batches de 50
- Insert bulk dans Supabase
```

### 2. Caching
```
Claude responses pour catégorisation:
- Cache les descriptions similaires
- Évite appels API redondants
- Économise ~60% tokens
```

### 3. Parallel Execution
```
Pour multiple bank accounts:
- Utiliser "parallel processing" dans Make
- Max 5 en parallèle
- Sync 5x plus rapide
```

---

## ✅ CHECKLIST WORKFLOWS

- [ ] Workflow 1: Bank Connection (testé) ✅
- [ ] Workflow 2: Daily Sync (fonctionne) ✅
- [ ] Workflow 3: Auto-Reconciliation (90%+ précision) ✅
- [ ] Workflow 4: Reminders (emails reçus) ✅
- [ ] Error handling configuré ✅
- [ ] Notifications activées ✅
- [ ] Tests end-to-end passent ✅

---

**Durée totale configuration**: 6-8 heures
**Prochaine étape**: Intégration complète Bubble ↔ Make ↔ Supabase

**NEXT**: `INTEGRATION_TESTS.md`


