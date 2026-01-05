# 🚀 DÉMARRAGE IMMÉDIAT - FinanceAI MVP

## ⏱️ TEMPS TOTAL: 4 heures pour avoir un MVP testable

---

## ✅ CHECKLIST RAPIDE

Cocher au fur et à mesure:

### PHASE 1: Comptes (90 min)
- [ ] Supabase créé + DB schema appliqué
- [ ] Bridge API (sandbox) configuré
- [ ] Claude API testée
- [ ] SendGrid vérifié
- [ ] Stripe products créés
- [ ] Bubble.io app créée (plan Starter payé)
- [ ] Make.com compte créé (plan Core payé)
- [ ] .env rempli avec TOUTES les clés

### PHASE 2: Bubble Structure (60 min)
- [ ] 6 data types créés
- [ ] Privacy rules activées
- [ ] 3 pages essentielles: signup, login, dashboard
- [ ] 1 workflow signup fonctionnel
- [ ] Test: Inscription → Login → Dashboard ✅

### PHASE 3: Make Workflow 1 (45 min)
- [ ] Workflow "Bank Connection" créé
- [ ] Webhook URL copié dans .env
- [ ] Module Bridge API configuré
- [ ] Test curl fonctionne

### PHASE 4: Make Workflow 2 (45 min)
- [ ] Workflow "Sync Transactions" créé
- [ ] Supabase + Bridge + Claude connectés
- [ ] Test: Déclenche manuellement → Transactions dans DB ✅

---

## 🎯 TEST END-TO-END MINIMAL (30 min)

**Objectif**: Prouver que tout fonctionne ensemble

### Étape 1: Créer un compte
```
1. Ouvrir Bubble app: https://financeai.bubbleapps.io
2. Cliquer "Créer un compte"
3. Email: test@financeai.fr
4. Password: Test123!
5. Company: Test Corp
6. → Devrait rediriger vers dashboard
```

### Étape 2: Connecter une banque (Sandbox Bridge)
```
1. Dashboard → "Connecter une banque"
2. Bridge modal s'ouvre
3. Sélectionner: "Demo Bank" (banque de test)
4. Credentials: demo / demo
5. → Devrait créer un BankAccount dans Supabase
```

### Étape 3: Synchroniser les transactions
```
1. Make.com → Workflow "Sync Transactions"
2. "Run once" (manuel)
3. Vérifier logs:
   - Bridge API: ✅ Transactions fetched
   - Claude API: ✅ Categorized
   - Supabase: ✅ Inserted
4. Retour dans Bubble → Page "Transactions"
5. → Devrait afficher les transactions de test
```

### ✅ SUCCESS CRITERIA
- [ ] Compte créé
- [ ] Banque connectée (même sandbox)
- [ ] Transactions affichées dans l'interface
- [ ] Catégories IA assignées

**SI TOUT PASSE**: MVP fonctionnel à 30% → Continuer features

**SI BLOQUÉ**: Checker les logs (détails plus bas)

---

## 🐛 DEBUG RAPIDE

### Problème: "Signup ne fonctionne pas"
```
Bubble Debugger (Step-by-step mode):
1. Ouvrir page signup
2. Activer debugger (bottom left)
3. Remplir form + Submit
4. Vérifier logs:
   - "Sign the user up" → Email/password OK?
   - "Create User" → Fields remplis?
   - Erreur? → Lire message exact

Fix communs:
- Email déjà utilisé → Changer email
- Password too weak → Min 8 chars
- Privacy rules trop strictes → Temporarily disable
```

### Problème: "Bridge API ne répond pas"
```
Test direct:
curl -X POST https://api.bridgeapi.io/v2/authenticate \
  -H "Content-Type: application/json" \
  -H "Client-Id: YOUR_CLIENT_ID" \
  -H "Client-Secret: YOUR_CLIENT_SECRET" \
  -H "Bridge-Version: 2021-06-01" \
  -d '{"email": "test@test.com", "password": "test"}'

Erreurs possibles:
- 401: Mauvaise API key → Re-check dashboard
- 403: Compte pas activé → Verify email
- 500: Sandbox down → Attendre 5 min
```

### Problème: "Claude ne catégorise pas"
```
Test direct:
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Test"}]
  }'

Erreurs:
- 401: Mauvaise clé API
- 429: Rate limit → Wait 1 min
- Response pas JSON → Vérifier prompt dans Make
```

### Problème: "Supabase INSERT échoue"
```
Vérifier:
1. Supabase Dashboard → Table Editor → Transactions
2. Insert manual: [+ Insert row]
3. Si erreur:
   - Constraint violation? → Check schema
   - Permission denied? → Check RLS policies
   - Column missing? → Re-run schema SQL

Quick fix RLS (temporaire, DEV ONLY):
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public access" ON transactions FOR ALL USING (true);
```

### Problème: "Make workflow erreur"
```
Make Logs:
1. Workflow → History
2. Cliquer sur dernière exécution (rouge = erreur)
3. Voir quel module a échoué
4. Cliquer sur module → Voir détails erreur

Fix communs:
- Module HTTP 400: Body mal formaté → Check JSON syntax
- Module HTTP 401: API key manquante → Re-add header
- Module HTTP 500: API down → Retry later
- Timeout: Requête trop longue → Augmenter timeout (Settings)
```

---

## 📊 DASHBOARD MONITORING

### Métriques à suivre (après MVP fonctionne)

**Supabase**:
```
SELECT COUNT(*) FROM users;          -- Combien d'utilisateurs?
SELECT COUNT(*) FROM bank_accounts;  -- Combien de banques?
SELECT COUNT(*) FROM transactions;   -- Combien de transactions?
SELECT COUNT(*) FROM reconciliations WHERE validated_by = 'ai'; -- Précision IA?
```

**Make.com**:
- Dashboard → Operations used / 10,000
- Si > 8,000 → Upgrade plan

**Claude API**:
- Console Anthropic → Usage
- Tokens utilisés / jour
- Si > 50k/jour → Optimiser prompts

**Bubble.io**:
- Capacity tab → Workload
- Si > 80% → Optimize workflows

---

## 🚦 GO / NO-GO DECISION (Fin Jour 1)

### ✅ GO (Continuer développement)
- [ ] Tous les comptes créés
- [ ] .env complet
- [ ] Bubble: Signup/Login fonctionne
- [ ] Make: Au moins 1 workflow teste OK
- [ ] Supabase: Données insérées manuellement OK

**→ NEXT**: Continuer JOUR 2-3 (Bubble structure complète)

### ❌ NO-GO (Problème bloquant)
- [ ] API key ne fonctionne pas (après 3 tentatives)
- [ ] Supabase DB schema erreur (violations)
- [ ] Bubble workflows ne se déclenchent pas

**→ FIX**: 
1. Poster dans Discord communauté (Bubble/Make)
2. Checker status pages: status.supabase.io, bridgeapi.io/status
3. Contacter support (Bubble: chat, Make: email)

---

## 💡 TIPS PRODUCTIVITÉ

### 1. Dual Screen
- Screen 1: Bubble.io editor
- Screen 2: Make.com editor + Documentation

### 2. Browser Tabs
```
Tab 1: Bubble editor
Tab 2: Bubble debugger (preview mode)
Tab 3: Make.com
Tab 4: Supabase Dashboard → Table Editor
Tab 5: Cette doc (DEMARRAGE_IMMEDIAT.md)
```

### 3. Keyboard Shortcuts
```
Bubble:
- Cmd/Ctrl + K: Search elements
- Cmd/Ctrl + C/V: Copy/paste elements
- Cmd/Ctrl + Z: Undo

Make:
- Cmd/Ctrl + S: Save scenario
- Cmd/Ctrl + Enter: Run scenario
```

### 4. Version Control
```bash
# Commit après chaque milestone
git add .
git commit -m "feat: Bubble structure complete"
git push

# Créer branches pour features
git checkout -b feature/reconciliation
```

---

## 🎯 OBJECTIF FIN JOUR 1

**Livrable**:
- [ ] Infrastructure complète (comptes créés)
- [ ] Bubble: Login/Signup fonctionne
- [ ] Make: 1 workflow teste OK
- [ ] Test end-to-end minimal réussi

**État mental**: 
- ✅ "J'ai prouvé que c'est faisable"
- ✅ "Les APIs fonctionnent ensemble"
- ✅ "Je peux continuer sereinement"

**Celebration**: 🎉 Café bien mérité !

---

## 📞 SUPPORT

**Besoin d'aide?**
- Bubble: https://forum.bubble.io (réponse < 1h)
- Make: https://community.make.com
- Supabase: https://github.com/supabase/supabase/discussions
- Bridge API: support@bridgeapi.io

**Emergency contacts** (si bloqué > 2h):
- [À définir: Votre contact technique de backup]

---

**READY?** Ouvrir `PLAN_DEV_IMMEDIAT.md` → JOUR 1 → GO! 🚀


