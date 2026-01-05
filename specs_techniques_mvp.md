# Spécifications Techniques MVP - Top 3 Niches

## Philosophie MVP: "Do Things That Don't Scale" (Paul Graham)

**Objectifs MVP**:
1. ✅ Valider product-market fit (pas perfection technique)
2. ✅ Time-to-market < 6 semaines
3. ✅ Budget < 3,000€ par MVP
4. ✅ Scalable ultérieurement (pas de tech debt bloquante)

---

## MVP #1: AUTOMATISATION FINANCE PME

### Architecture Globale

```
[Utilisateur] → [Frontend No-Code] → [Make.com Orchestration] → [Claude API + Banking APIs] → [Database] → [Intégrations Comptables]
```

### Stack Technique Recommandée

#### Option A: No-Code (Recommandé Phase 1)

**Frontend**:
- **Outil**: Bubble.io ou FlutterFlow
- **Coût**: 29-50€/mois
- **Justification**: Interface utilisateur rapide, auth intégré, responsive
- **Pages**: Dashboard, Connexion banques, Rapprochements, Factures, Settings

**Backend/Orchestration**:
- **Outil**: Make.com (99€/mois plan Pro)
- **Workflows**:
  1. Sync bancaire quotidien (DSP2 APIs)
  2. Rapprochement automatique (matching transactions ↔ factures)
  3. Génération relances factures
  4. Calcul prévisions trésorerie
  5. Exports comptables

**Intelligence IA**:
- **LLM**: Claude 3.5 Sonnet (Anthropic API)
- **Coût**: ~$3/1M tokens input, ~$15/1M output
- **Usage estimé**: 50-100€/mois pour 20 clients
- **Use cases**:
  - Catégorisation transactions intelligente
  - Matching factures ↔ paiements (fuzzy logic)
  - Génération emails relances personnalisés
  - Détection anomalies

**Base de Données**:
- **Outil**: Supabase (gratuit → 25€/mois)
- **Tables**:
  - users (clients)
  - bank_accounts
  - transactions
  - invoices
  - reconciliations
  - forecasts

**Intégrations Bancaires**:
- **API**: Bridge API ou Bankin' (agrégateurs DSP2)
- **Coût**: 0.10-0.30€ par sync
- **Banques supportées**: 300+ banques françaises
- **Sécurité**: OAuth 2.0, encryption at rest

**Intégrations Comptables**:
- **Priorité 1**: Pennylane API (moderne, bien documentée)
- **Priorité 2**: Sage API
- **Priorité 3**: QuickBooks API
- **Format export**: FEC (Fichier Écritures Comptables) standard

**Hébergement**:
- **Frontend**: Bubble hosting inclus
- **Workflows**: Make.com cloud
- **Database**: Supabase cloud
- **Coût total**: 0-20€/mois

#### Option B: Code (Si expertise technique)

**Stack**:
- **Backend**: Python FastAPI
- **Frontend**: Next.js 15 + React
- **Database**: PostgreSQL (Supabase)
- **Queue**: Celery + Redis (tâches asynchrones)
- **Deploy**: Railway ou Fly.io (20-50€/mois)

**Avantages**: Plus flexible, meilleures performances
**Inconvénients**: Développement 2-3x plus long

### Features MVP (Phase 1 - 6 semaines)

#### Must-Have (Semaines 1-4)

1. **Connexion Bancaire**
   - Onboarding: Connexion 1-3 comptes bancaires via Bridge API
   - Sync automatique quotidien
   - Historique 3 mois

2. **Rapprochement Automatique**
   - Matching transactions ↔ factures (règles + IA)
   - Suggestions avec score confiance (0-100%)
   - Validation manuelle si score < 80%
   - Export réconciliations

3. **Relances Factures**
   - Import factures (CSV ou intégration comptable)
   - Détection factures impayées
   - Génération emails relances (templates + IA personnalisation)
   - Tracking ouvertures/clics

4. **Dashboard**
   - Vue trésorerie actuelle
   - Factures en attente
   - Réconciliations à valider
   - Prochaines échéances

#### Nice-to-Have (Semaines 5-6)

5. **Prévisions Trésorerie**
   - Projection 3 mois basée historique
   - Scénarios (optimiste/pessimiste)
   - Alertes seuils

6. **Catégorisation Intelligente**
   - Auto-catégorisation dépenses (IA)
   - Apprentissage corrections utilisateur

### Workflow Technique Détaillé

#### Workflow 1: Sync Bancaire (Quotidien)

```
Trigger: Cron 6h00 daily
│
├─ Pour chaque client actif:
│  ├─ Appel Bridge API (get transactions)
│  ├─ Déduplication (check existing transactions)
│  ├─ Insert nouvelles transactions DB
│  ├─ Catégorisation IA (Claude)
│  └─ Notification client si anomalies
│
└─ Log résultats + erreurs
```

#### Workflow 2: Rapprochement Automatique (Trigger: Nouvelle transaction)

```
Trigger: Nouvelle transaction bancaire
│
├─ Récupérer factures impayées client
│
├─ Matching Algorithm:
│  ├─ Exact match (montant + date ±3j + référence)
│  ├─ Fuzzy match (Claude: analyse libellé vs facture)
│  └─ Score confiance 0-100%
│
├─ Si score > 80%:
│  └─ Auto-réconciliation
│
├─ Si score 50-80%:
│  └─ Suggestion utilisateur (validation requise)
│
└─ Si score < 50%:
   └─ Pas de suggestion (manuel)
```

#### Workflow 3: Relances Factures (Hebdomadaire)

```
Trigger: Lundi 9h00
│
├─ Pour chaque client:
│  ├─ Identifier factures impayées > 7j échéance
│  │
│  ├─ Pour chaque facture:
│  │  ├─ Check historique relances (éviter spam)
│  │  ├─ Génération email personnalisé (Claude)
│  │  │  - Ton adapté (courtois J+7, ferme J+30)
│  │  │  - Contexte client
│  │  │  - Montant, référence, échéance
│  │  │
│  │  ├─ Envoi email (SMTP ou SendGrid)
│  │  └─ Log relance DB
│  │
│  └─ Notification client (résumé relances envoyées)
```

### Coûts Techniques MVP (Mensuels)

| Composant | Coût Fixe | Coût Variable | Total (20 clients) |
|-----------|-----------|---------------|---------------------|
| Bubble.io | 29€ | - | 29€ |
| Make.com | 99€ | - | 99€ |
| Supabase | 25€ | - | 25€ |
| Claude API | - | 2-3€/client | 50€ |
| Bridge API | - | 3€/client | 60€ |
| SendGrid | 15€ | 0.10€/email | 25€ |
| **TOTAL** | **168€** | **~120€** | **~290€** |

**Marge brute** (20 clients à 499€/mois): 9,980€ - 290€ = **9,690€ (97%)**

### Sécurité & Compliance

**Critiques**:
- ✅ **RGPD**: Consentement explicite, droit à l'oubli, portabilité données
- ✅ **PCI-DSS**: Pas de stockage données bancaires sensibles (via Bridge)
- ✅ **Encryption**: At rest (Supabase) + in transit (HTTPS/TLS)
- ✅ **Auth**: OAuth 2.0, MFA optionnel
- ✅ **Backup**: Supabase automatic backups daily

**Mentions Légales**:
- CGU/CGV claires
- Politique confidentialité
- Disclaimer: "Outil d'aide, pas de conseil comptable"

---

## MVP #2: CONTENT REPURPOSING MULTI-FORMAT

### Architecture

```
[User Upload] → [Frontend] → [Make.com] → [Claude API] → [Formatting] → [Output Delivery]
```

### Stack Technique

#### Frontend
- **Outil**: Framer (templates créateurs) ou Webflow
- **Coût**: 15-30€/mois
- **Features**:
  - Upload article (URL ou texte)
  - Sélection formats sortie (checkboxes)
  - Customisation ton de voix
  - Preview outputs
  - Download/Copy

#### Backend
- **Orchestration**: Make.com (39-99€/mois)
- **LLM**: Claude 3.5 Sonnet
- **Storage**: Google Drive ou S3 (outputs)

#### Workflow

```
1. User uploads article (URL ou paste text)
   │
2. Extraction contenu (si URL):
   ├─ Scraping (Apify ou Jina Reader API)
   └─ Cleaning HTML → plain text
   │
3. Analyse contenu (Claude):
   ├─ Extraction points clés
   ├─ Identification ton de voix
   └─ Structuration thèmes
   │
4. Génération formats (parallèle):
   ├─ LinkedIn post (1200 chars)
   ├─ X/Twitter thread (10 tweets)
   ├─ Newsletter section (500 words)
   ├─ YouTube script (5 min)
   ├─ Instagram carousel (10 slides texte)
   ├─ Blog summary (300 words)
   ├─ Email subject lines (5 variants)
   ├─ Meta descriptions SEO (3 variants)
   ├─ Quotes extraits (10 quotes)
   └─ Hashtags (20 relevant)
   │
5. Formatting & Delivery:
   ├─ Markdown formatting
   ├─ Preview interface
   └─ Download ZIP ou Copy individual
```

### Features MVP

**Must-Have**:
1. Upload article (URL ou texte, max 5000 words)
2. Génération 10 formats automatique
3. Preview tous formats
4. Copy to clipboard / Download
5. Historique repurposing (last 10)

**Nice-to-Have**:
6. Customisation ton de voix (analyse écrits passés)
7. Scheduling posts (intégration Buffer)
8. Brand voice training (upload 3-5 articles existants)

### Coûts Techniques

| Composant | Coût Fixe | Coût Variable | Total (50 users) |
|-----------|-----------|---------------|------------------|
| Framer | 20€ | - | 20€ |
| Make.com | 39€ | - | 39€ |
| Claude API | - | 0.50€/repurposing | 250€ (10 repurposing/user) |
| Storage | 5€ | - | 5€ |
| **TOTAL** | **64€** | **~250€** | **~315€** |

**Revenus** (50 users à 99€/mois): 4,950€
**Marge brute**: 4,950€ - 315€ = **4,635€ (94%)**

---

## MVP #3: MONITORING CONCURRENCE + VEILLE

### Architecture

```
[User Setup] → [Scraping Engine] → [Change Detection] → [AI Analysis] → [Alerts] → [Dashboard]
```

### Stack Technique

#### Frontend
- **Outil**: Bubble.io ou Next.js
- **Features**:
  - Setup concurrents (URLs)
  - Configuration alertes
  - Dashboard changements
  - Rapports hebdomadaires

#### Scraping & Monitoring
- **Engine**: Apify (actors pré-faits) ou Browse AI
- **Coût**: 49-199€/mois (usage-based)
- **Fréquence**: Daily scraping

#### Intelligence
- **Change Detection**: Algorithme diff (text similarity)
- **AI Analysis**: Claude pour identifier changements significatifs
- **Categorization**: Prix, produits, contenu, design, features

#### Alerting
- **Channels**: Email, Slack, webhook
- **Frequency**: Real-time (critiques) ou daily digest

### Workflow

```
Daily Cron 2h00:
│
├─ Pour chaque client:
│  ├─ Pour chaque concurrent configuré:
│  │  ├─ Scrape pages (Apify)
│  │  ├─ Compare vs version précédente (DB)
│  │  ├─ Detect changes (text diff)
│  │  │
│  │  ├─ Si changements détectés:
│  │  │  ├─ AI Analysis (Claude):
│  │  │  │  - Type changement (prix, produit, contenu)
│  │  │  │  - Significance score (0-100)
│  │  │  │  - Summary changement
│  │  │  │
│  │  │  ├─ Si significance > 70:
│  │  │  │  └─ Alert immédiate (email/Slack)
│  │  │  │
│  │  │  └─ Store changement DB
│  │  │
│  │  └─ Update snapshot DB
│  │
│  └─ Génération rapport hebdomadaire (Lundi)
```

### Features MVP

**Must-Have**:
1. Add concurrents (URLs)
2. Daily monitoring automatique
3. Change detection (prix, contenu)
4. Email alerts changements significatifs
5. Dashboard historique changements

**Nice-to-Have**:
6. Competitive analysis (comparaison features)
7. Pricing trends (graphiques évolution)
8. SEO monitoring (keywords ranking)

### Coûts Techniques

| Composant | Coût Fixe | Coût Variable | Total (20 clients) |
|-----------|-----------|---------------|---------------------|
| Bubble.io | 29€ | - | 29€ |
| Apify | 99€ | 2€/client | 140€ |
| Claude API | - | 1€/client | 20€ |
| Supabase | 25€ | - | 25€ |
| SendGrid | 15€ | - | 15€ |
| **TOTAL** | **168€** | **~60€** | **~230€** |

**Revenus** (20 clients à 399€/mois): 7,980€
**Marge brute**: 7,980€ - 230€ = **7,750€ (97%)**

---

## COMPARAISON STACKS: NO-CODE VS CODE

### No-Code (Recommandé MVP)

**Avantages**:
- ✅ Time-to-market: 3-6 semaines
- ✅ Coût développement: 0€ (DIY) ou 1,000-2,000€ (freelance)
- ✅ Maintenance simple
- ✅ Itérations rapides
- ✅ Pas besoin CTO

**Inconvénients**:
- ⚠️ Limites customisation
- ⚠️ Coûts fixes élevés (outils SaaS)
- ⚠️ Vendor lock-in
- ⚠️ Scaling limité (> 500 clients)

**Verdict**: **Parfait pour validation PMF** (0-100 clients)

### Code (Pour Scaling)

**Avantages**:
- ✅ Contrôle total
- ✅ Coûts variables optimisés
- ✅ Performance supérieure
- ✅ Scaling illimité

**Inconvénients**:
- ❌ Time-to-market: 8-16 semaines
- ❌ Coût développement: 5,000-15,000€
- ❌ Maintenance complexe
- ❌ Nécessite CTO/dev

**Verdict**: **Migration après 100+ clients** ou levée de fonds

---

## STRATÉGIE MIGRATION NO-CODE → CODE

**Trigger Migration**:
- 100+ clients actifs
- Revenus > 15K€/mois
- Coûts no-code > 1,000€/mois
- Limites techniques bloquantes

**Approche**:
1. **Phase 1**: Backend migration (APIs, workflows)
2. **Phase 2**: Frontend migration (progressive)
3. **Phase 3**: Décommission no-code tools

**Coût migration**: 10,000-20,000€
**Durée**: 3-4 mois

---

*Document généré: Janvier 2026*
*Prochaine étape: Modèle économique et projections financières*


