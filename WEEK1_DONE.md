# ✅ SEMAINE 1 - VALIDATION ÉTAPE PAR ÉTAPE

## 🎯 Objectif: MVP No-Code fonctionnel

---

## JOUR 1: Infrastructure ✅

### Checkpoint 1: Comptes API (2h)
```bash
# Tester chaque API individuellement
./scripts/test_apis.sh

Expected output:
✅ Supabase: Connected (8 tables visible)
✅ Bridge API: Authenticated
✅ Claude API: Response received
✅ SendGrid: Test email sent
✅ Stripe: Products listed
```

**Validation**:
- [ ] 8/8 tables Supabase visibles
- [ ] Bridge sandbox login fonctionne
- [ ] Claude répond en < 5s
- [ ] Email test reçu dans inbox
- [ ] 3 products Stripe créés

**Commit**:
```bash
git add .env docs/api-setup.md
git commit -m "chore: Configure all external APIs"
# NE PAS PUSH .env !
```

---

## JOUR 2: Bubble Structure ✅

### Checkpoint 2: Data Model (1h)
**Supabase Table Editor**:
```sql
-- Vérifier que ces queries fonctionnent:
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM bank_accounts;
SELECT COUNT(*) FROM transactions;
SELECT COUNT(*) FROM invoices;
SELECT COUNT(*) FROM reconciliations;
SELECT COUNT(*) FROM reminders;
SELECT COUNT(*) FROM audit_logs;
SELECT COUNT(*) FROM user_preferences;
```

**Bubble Data Types**:
- Ouvrir Bubble → Data → Data types
- Vérifier: 6 types créés (User, BankAccount, Transaction, Invoice, Reconciliation, Reminder)
- Vérifier: Privacy rules activées pour TOUS les types

**Validation**:
- [ ] 8 tables Supabase existent
- [ ] 6 data types Bubble créés
- [ ] Privacy rules = 100% couverture
- [ ] Test: "This User's" filter fonctionne

---

### Checkpoint 3: Pages & Navigation (2h)

**Créer compte test**:
```
Email: test@financeai.fr
Password: Test123!
Company: Test Corp
```

**Tester navigation**:
1. Page index (not logged) → Header + CTA visible ✅
2. Click "Démarrer" → Redirect to signup ✅
3. Fill signup form → Submit → Redirect to dashboard ✅
4. Dashboard → Sidebar visible with 6 links ✅
5. Click each link → Page loads (can be empty) ✅
6. Click "Déconnexion" → Redirect to index ✅

**Validation**:
- [ ] 9 pages créées
- [ ] Navigation sidebar fonctionne
- [ ] Signup → Login → Dashboard flow OK
- [ ] Privacy: User A ne voit pas data de User B

**Screenshot**:
```bash
# Prendre screenshots de:
- Dashboard (logged in)
- Page transactions (même vide)
- Page invoices (même vide)

# Sauvegarder dans:
docs/screenshots/week1/
```

---

### Checkpoint 4: Workflows Bubble (2h)

**Test Workflow 1: Signup**
```
1. Page signup → Remplir form
2. Open Bubble Debugger (step-by-step mode)
3. Click "Créer mon compte"
4. Vérifier steps:
   - Step 1: "Sign the user up" → Success ✅
   - Step 2: "Create User" → User created ✅
   - Step 3: "Navigate to dashboard" → Redirected ✅
5. Check Supabase: New user dans table users ✅
```

**Test Workflow 2: Login**
```
1. Logout
2. Page login → Email + Password
3. Debugger on
4. Submit
5. Steps:
   - "Log the user in" → Success ✅
   - "Navigate to dashboard" → Redirected ✅
```

**Validation**:
- [ ] Signup crée user dans Bubble + Supabase
- [ ] Login redirige vers dashboard
- [ ] Session persiste (refresh page → toujours logged)
- [ ] Logout déconnecte vraiment

---

## JOUR 3: Make.com Workflows ✅

### Checkpoint 5: Workflow Bank Connection (1h)

**Setup**:
```
1. Make.com → Scenario "Bank Connection Flow"
2. Add modules:
   - Webhook (trigger)
   - HTTP: Bridge API Generate Connect URL
   - HTTP Response
3. Save → Activate
4. Copy webhook URL → .env
```

**Test**:
```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-uuid-123"}'

Expected response:
{
  "success": true,
  "connect_url": "https://connect.bridgeapi.io/...",
  "connect_token": "xxx"
}
```

**Validation**:
- [ ] Webhook déclenche le scenario
- [ ] Bridge API répond (status 200)
- [ ] connect_url valide retournée
- [ ] Make logs: 3/3 modules success

---

### Checkpoint 6: Workflow Sync Transactions (3h)

**Setup**:
```
1. Scenario "Daily Sync Transactions"
2. Add 12 modules (voir MAKE_WORKFLOWS_SETUP.md)
3. Configure TOUS les headers/body
4. Save → Activate
```

**Test manuel**:
```
1. Supabase: Insert manual bank account
   - user_id: [votre test user id]
   - bridge_account_id: "demo_account_123"
   - bank_name: "Demo Bank"
   - is_active: true

2. Make: "Run once" (manual trigger)

3. Watch logs in real-time:
   - Module 2: Supabase query → 1 account found ✅
   - Module 4: Bridge API → Transactions fetched ✅
   - Module 8A: Claude → Categorization response ✅
   - Module 10A: Supabase → Transaction inserted ✅

4. Verify Supabase: SELECT * FROM transactions;
   → Au moins 1 transaction avec category ✅
```

**Validation**:
- [ ] Workflow s'exécute sans erreur
- [ ] Bridge API retourne transactions
- [ ] Claude catégorise correctement
- [ ] Transactions insérées dans Supabase
- [ ] Champ "category" rempli (not null)

---

### Checkpoint 7: Intégration Bubble ↔ Make ↔ Supabase (2h)

**Flow complet**:
```
1. Bubble Dashboard → Button "Synchroniser"
2. Workflow Bubble:
   - Call Make webhook (Sync Transactions)
   - Show loading spinner
3. Make workflow exécute (voir Checkpoint 6)
4. Bubble:
   - Wait for completion (polling or callback)
   - Refresh Repeating Group "Transactions"
5. User voit: Liste de transactions avec catégories ✅
```

**Setup Bubble Workflow**:
```
Trigger: Button "Synchroniser" is clicked

Step 1: Set state "is_syncing" = yes

Step 2: API Connector - POST to Make webhook
  URL: <MAKE_WEBHOOK_SYNC>
  Body: {"bank_account_id": "This BankAccount's id"}

Step 3: Pause (2 seconds) [simple polling for MVP]

Step 4: Refresh Repeating Group "Transactions"

Step 5: Set state "is_syncing" = no

Step 6: Show notification "X transactions synchronisées"
```

**Test end-to-end**:
```
1. Bubble: Page bank-accounts
2. Click "Synchroniser maintenant"
3. Vérifier:
   - Loading spinner appears ✅
   - Make scenario s'exécute (check logs) ✅
   - Spinner disappears ✅
   - Toast notification "Synchronisé" ✅
   - Page transactions: Nouvelles transactions visibles ✅
```

**Validation**:
- [ ] Button déclenche Make webhook
- [ ] Make workflow s'exécute
- [ ] Bubble affiche les nouvelles transactions
- [ ] UX: Loading states + notifications
- [ ] Pas d'erreur console browser

---

## JOUR 4-5: Features Avancées ✅

### Checkpoint 8: Auto-Reconciliation (3h)

**Setup Make Workflow** (voir `MAKE_WORKFLOWS_SETUP.md`):
- Webhook trigger
- Get transaction details
- Get unpaid invoices
- Calculate match scores (exact + fuzzy)
- Claude AI fuzzy matching
- Create reconciliations

**Préparer test data**:
```sql
-- Supabase SQL Editor
-- 1. Créer une transaction
INSERT INTO transactions (
  id, bank_account_id, date, description, amount, category, is_reconciled
) VALUES (
  gen_random_uuid(),
  '<YOUR_BANK_ACCOUNT_ID>',
  '2026-01-03',
  'VIR CLIENT ACME CORP - FACTURE F2024-001',
  1500.00,
  'Clients',
  false
);

-- 2. Créer une invoice correspondante
INSERT INTO invoices (
  id, user_id, invoice_number, client_name, amount, due_date, status, is_reconciled
) VALUES (
  gen_random_uuid(),
  '<YOUR_USER_ID>',
  'F2024-001',
  'ACME Corp',
  1500.00,
  '2026-01-05',
  'pending',
  false
);
```

**Test**:
```bash
# Déclencher reconciliation
curl -X POST "YOUR_MAKE_WEBHOOK_RECONCILE" \
  -H "Content-Type: application/json" \
  -d '{"transaction_id": "<TRANSACTION_ID>"}'

# Vérifier logs Make:
- Module: Get Transaction → Found ✅
- Module: Get Invoices → 1 found ✅
- Module: Calculate Score → 1.0 (exact match) ✅
- Module: Create Reconciliation → Success ✅

# Vérifier Supabase:
SELECT * FROM reconciliations WHERE transaction_id = '<ID>';
→ 1 row, validated_by = 'ai' ✅

SELECT is_reconciled FROM transactions WHERE id = '<ID>';
→ true ✅

SELECT status FROM invoices WHERE invoice_number = 'F2024-001';
→ 'paid' ✅
```

**Validation**:
- [ ] Exact match détecté (score = 1.0)
- [ ] Reconciliation créée automatiquement
- [ ] Transaction & Invoice updated
- [ ] Claude fuzzy match fonctionne (test avec données non-exact)

---

### Checkpoint 9: Email Reminders (2h)

**Préparer test data**:
```sql
-- Invoice overdue (due_date dans le passé)
INSERT INTO invoices (
  id, user_id, invoice_number, client_name, client_email,
  amount, issue_date, due_date, status, is_reconciled
) VALUES (
  gen_random_uuid(),
  '<YOUR_USER_ID>',
  'F2024-OVERDUE',
  'Late Client',
  'your_test_email@gmail.com',  -- Votre vrai email pour test
  2500.00,
  '2025-11-01',
  '2025-12-15',  -- 20 jours en retard
  'pending',
  false
);
```

**Test workflow**:
```
1. Make: Scenario "Send Reminders"
2. "Run once" (manual trigger)
3. Vérifier logs:
   - Module 2: Get overdue invoices → 1 found ✅
   - Module 8: Claude generate email → JSON response ✅
   - Module 10: SendGrid → Email sent (status 202) ✅
   - Module 11: Reminder record created ✅

4. Check votre inbox:
   - Email reçu ✅
   - Subject professionnel ✅
   - Body en français, bien formaté ✅
   - Pas de fautes ✅
```

**Validation**:
- [ ] Invoice overdue détectée
- [ ] Claude génère email personnalisé
- [ ] SendGrid envoie (pas de bounce)
- [ ] Email reçu et professionnel
- [ ] Reminder enregistré dans DB

---

## JOUR 5: Polish & Tests ✅

### Checkpoint 10: UI/UX Polish (2h)

**Bubble improvements**:
```
1. Dashboard KPIs:
   - Solde total (sum bank_accounts.balance)
   - Factures impayées (count invoices where status=pending)
   - En attente réconciliation (count reconciliations where validated_by=null)

2. Transactions list:
   - Sort by date DESC
   - Filter by date range (date picker)
   - Badge "Réconciliée" si is_reconciled=true
   - Color code categories

3. Invoices list:
   - Badge status: pending(yellow), paid(green), overdue(red)
   - "Send reminder" button (only if overdue)
   - "Mark as paid" button

4. Loading states:
   - Show spinner when API calls
   - Disable buttons during loading

5. Error handling:
   - Show toast on error
   - Log errors to Supabase audit_logs
```

**Validation**:
- [ ] KPIs affichent vraies valeurs
- [ ] Listes: Tri + filtres fonctionnent
- [ ] Badges: Couleurs correctes
- [ ] Loading: Spinners visibles
- [ ] Errors: Messages clairs

---

### Checkpoint 11: Tests End-to-End (2h)

**Scenario 1: Onboarding complet**
```
1. Signup nouveau user
2. Dashboard vide s'affiche
3. "Connecter une banque" → Bridge modal
4. Sélectionner Demo Bank → Success
5. "Synchroniser" → Transactions importées
6. Vérifier catégories IA assignées
7. Check: bank_accounts, transactions tables populated

Time: ~5 min
Status: [ ] PASS / [ ] FAIL
```

**Scenario 2: Invoice → Reconciliation**
```
1. "Nouvelle facture" → Form
2. Fill: Client, Amount, Due date
3. Submit → Invoice créée
4. "Synchroniser transactions" → Import transaction matching
5. Auto-reconciliation detecte match
6. "Réconciliations" page → Suggestion visible
7. "Valider" → Invoice status = "paid"

Time: ~7 min
Status: [ ] PASS / [ ] FAIL
```

**Scenario 3: Reminder flow**
```
1. Créer invoice overdue (manual SQL)
2. Make: "Send Reminders" → Run once
3. Check inbox → Email reçu
4. Verify reminder record in DB

Time: ~3 min
Status: [ ] PASS / [ ] FAIL
```

**Validation**:
- [ ] 3/3 scenarios PASS
- [ ] Aucune erreur console
- [ ] Performance: Pages < 2s load time
- [ ] Mobile responsive (tester sur iPhone/Android)

---

## 🎯 FIN SEMAINE 1: GO/NO-GO

### ✅ GO (MVP validé)

**Critères**:
- [ ] Infrastructure 100% opérationnelle
- [ ] Bubble: Structure complète + navigable
- [ ] Make: 3+ workflows fonctionnels
- [ ] Tests E2E: 3/3 PASS
- [ ] Aucun bug bloquant

**Livrables**:
- [ ] App Bubble accessible (financeai.bubbleapps.io)
- [ ] Documentation à jour
- [ ] .env complet (backup sécurisé)
- [ ] Screenshots (avant/après)
- [ ] Video demo (2 min) [optionnel]

**Métriques**:
- Users: 1 (compte test)
- Bank Accounts: 1 (sandbox)
- Transactions: 10+ (test data)
- Invoices: 3+ (test data)
- Reconciliations: 1+ (auto)
- Reminders: 1+ (sent)

**Next**: SEMAINE 2 → First beta testers (3-5 vrais users)

---

### ❌ NO-GO (Problèmes bloquants)

**Si ces points échouent**:
- [ ] Bridge API ne se connecte pas (> 3 tentatives)
- [ ] Claude retourne erreurs systématiques
- [ ] Bubble workflows timeout constants
- [ ] Make scenarios erreur rate > 10%
- [ ] Tests E2E: 0/3 ou 1/3 PASS

**Actions**:
1. **STOP développement** nouvelles features
2. **DEBUG** intensif (1-2 jours max)
3. **PIVOT** si nécessaire:
   - Bridge down → Utiliser Plaid ou Tink
   - Claude expensive → GPT-4o mini
   - Bubble limits → Commencer migration code

4. **DECISION**: 
   - Fix possible sous 48h? → Fix puis GO
   - Impossible? → Replanning (voir ROADMAP_PLAN_B.md)

---

## 📊 DASHBOARD FINAL SEMAINE 1

**Temps investi**:
- Infrastructure: 4h ✅
- Bubble structure: 8h ✅
- Make workflows: 8h ✅
- Integration: 4h ✅
- Tests: 4h ✅
**TOTAL**: 28h (3.5 jours ouvrés)

**Budget dépensé**:
- Bubble Starter: 29€ ✅
- Make Core: 39€ ✅
- Supabase: 0€ (free tier) ✅
- Bridge sandbox: 0€ ✅
- Claude API: ~5€ (tests) ✅
- SendGrid: 0€ (free tier) ✅
**TOTAL**: 73€ / 2,000€ budget

**Coverage**:
- Core features: 80% ✅
- UX polish: 60% ⚠️
- Tests: 70% ✅
- Security: 50% ⚠️ (prod needs improvement)

**Prêt pour**: 
- [ ] Beta testers (5 early adopters)
- [ ] Feedback collection
- [ ] Iteration rapide

---

**CONGRATS! 🎉** MVP No-Code opérationnel en 1 semaine!

**Next steps**: `SEMAINE_2_BETA.md`

