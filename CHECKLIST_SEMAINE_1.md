# ✅ CHECKLIST SEMAINE 1 - Démarrage FinanceAI

## 📅 Jour 1-2: Validation Finale

### Landing Page (si pas déjà fait)
- [ ] Créer landing page (Carrd.co ou Framer)
  - [ ] Headline: "Automatisez votre comptabilité PME en 30 minutes"
  - [ ] 5 value props clairs
  - [ ] Pricing visible: 399-999€/mois
  - [ ] CTA: "Rejoindre liste d'attente"
  - [ ] Email capture (Tally.so)

### Ads & Trafic (Budget: 400€)
- [ ] Google Ads (200€)
  - [ ] Mots-clés: "automatisation comptable PME"
  - [ ] Cible: France, décideurs
  - [ ] Landing page URL configurée
  
- [ ] LinkedIn Ads (200€)
  - [ ] Cible: CFO, DAF, gérants PME
  - [ ] Sponsored content
  - [ ] Tracking conversions

### Objectif Jour 2
- [ ] 100+ visites landing page
- [ ] 30+ emails collectés
- [ ] 10+ demandes de démo

---

## 📅 Jour 3-4: Création Comptes

### Comptes SaaS à créer

#### 1. Supabase (Database) ✅
- [ ] Créer compte: https://supabase.com
- [ ] Créer projet: "financeai-prod"
- [ ] Noter: 
  - [ ] Project URL
  - [ ] Anon key
  - [ ] Service key
- [ ] Exécuter `database_schema.sql` dans SQL Editor
- [ ] Vérifier tables créées (8 tables)

#### 2. Bridge API (Banking) 🏦
- [ ] Créer compte: https://dashboard.bridgeapi.io
- [ ] Mode: Sandbox (gratuit)
- [ ] Noter:
  - [ ] Client ID
  - [ ] Client Secret
  - [ ] API Key
- [ ] Tester API avec curl (voir README_SETUP.md)
- [ ] Banques test disponibles: ✅

#### 3. Anthropic (Claude AI) 🤖
- [ ] Créer compte: https://console.anthropic.com
- [ ] Noter API Key
- [ ] Crédits gratuits: 5$ (OK pour tests)
- [ ] Tester avec curl (catégorisation transaction)
- [ ] Résultat test satisfaisant: ✅

#### 4. SendGrid (Emails) 📧
- [ ] Créer compte: https://sendgrid.com
- [ ] Plan: Free (100 emails/jour)
- [ ] Créer API Key
- [ ] Vérifier domaine financeai.fr (éviter spam)
- [ ] Test email envoyé: ✅

#### 5. Stripe (Paiements) 💳
- [ ] Créer compte: https://stripe.com
- [ ] Mode: Test
- [ ] Noter:
  - [ ] Public key (pk_test_...)
  - [ ] Secret key (sk_test_...)
- [ ] Créer 3 produits:
  - [ ] Starter: 399€/mois
  - [ ] Pro: 699€/mois
  - [ ] Business: 999€/mois

#### 6. Bubble.io (Frontend) 🎨
- [ ] Créer compte: https://bubble.io
- [ ] Plan: Starter (29€/mois)
- [ ] Créer app: "FinanceAI"
- [ ] Custom domain: financeai.fr (configuration DNS)

#### 7. Make.com (Workflows) ⚙️
- [ ] Créer compte: https://make.com
- [ ] Plan: Core (39€/mois) ou Pro (99€/mois)
- [ ] Créer organization: "FinanceAI"

---

## 📅 Jour 5: Configuration Variables

### Fichier Environment
- [ ] Créer fichier `.env` (copier depuis `env.template`)
- [ ] Remplir TOUTES les variables:
  - [ ] Supabase (URL, keys)
  - [ ] Bridge API (client ID, secret, API key)
  - [ ] Anthropic (API key)
  - [ ] SendGrid (API key, from email)
  - [ ] Stripe (public, secret keys)
  - [ ] App URL
- [ ] Vérifier: fichier `.env` dans `.gitignore` ✅
- [ ] JAMAIS commit ce fichier!

### Tests Intégrations
```bash
# Test Supabase
psql DATABASE_URL -c "SELECT COUNT(*) FROM users;"

# Test Bridge API (voir README_SETUP.md pour curl)

# Test Claude API (voir README_SETUP.md pour curl)

# Test SendGrid (envoyer email test)
```

- [ ] Toutes les APIs répondent: ✅

---

## 📅 Jour 6-7: Interviews Prospects

### Préparer Interviews
- [ ] Script questions (voir `validation_strategy.md`)
- [ ] Calendly configuré
- [ ] Zoom/Google Meet prêt
- [ ] Incentive: 30€ Amazon (10 cartes achetées)

### Recruter 15-20 Prospects
- [ ] Emails liste d'attente (30 contacts)
- [ ] LinkedIn outreach (100 messages)
- [ ] Groupes Facebook entrepreneurs (posts)
- [ ] Réseau personnel (warm intros)

### Conduire Interviews
Objectifs:
- [ ] Interview 1: ✅ - Notes: ___
- [ ] Interview 2: ✅ - Notes: ___
- [ ] Interview 3: ✅ - Notes: ___
- [ ] ... (continuer jusqu'à 15-20)

### Synthèse Interviews
- [ ] Pain points confirmés: ✅
- [ ] WTP moyen: ___€/mois
- [ ] "Would definitely use": ___%
- [ ] Freins identifiés: ___
- [ ] Features must-have: ___

---

## 📅 Fin Semaine 1: Décision GO/NO-GO

### Critères GO
- [ ] **30+ emails** liste d'attente: ___ emails ✅/❌
- [ ] **60%+ "would use"** interviews: ___% ✅/❌
- [ ] **WTP > 400€/mois**: ___€ ✅/❌
- [ ] **5+ pre-sales**: ___ pre-sales ✅/❌

### Si GO ✅
**Action**: Continuer → Semaine 2 (Bubble.io + Make.com setup)

Prochaines étapes:
1. Lancer Founder Pass (199€/mois lifetime)
2. Onboarder 5-10 clients fondateurs
3. Commencer développement MVP no-code

### Si NO-GO ❌
**Action**: Pivot ou pause

Options:
1. Pivoter vers niche #2 (Content Repurposing)
2. Ajuster pricing (299€ au lieu de 399€?)
3. Affiner positionnement (ultra-niche: comptables uniquement?)
4. Pause et recherche complémentaire

---

## 📊 Métriques à Tracker

| Métrique | Cible | Actuel | Status |
|----------|-------|--------|--------|
| Visites landing page | 500+ | ___ | ⏳ |
| Taux conversion email | 3%+ | ___% | ⏳ |
| Emails collectés | 30+ | ___ | ⏳ |
| Interviews complétées | 15+ | ___ | ⏳ |
| "Would definitely use" | 60%+ | ___% | ⏳ |
| WTP moyen | 400€+ | ___€ | ⏳ |
| Pre-sales confirmées | 5+ | ___ | ⏳ |
| Budget dépensé | 500€ | ___€ | ⏳ |

---

## 🆘 Support

**Bloqué sur une étape?**
- Supabase: https://supabase.com/docs
- Bridge API: https://docs.bridgeapi.io
- Anthropic: https://docs.anthropic.com
- Questions roadmap: Voir `ROADMAP_FINANCE_PME.md`

**Next**: Semaine 2 → `CHECKLIST_SEMAINE_2.md` (à créer)

---

**Courage! La semaine la plus importante du projet. Let's go! 🚀**

