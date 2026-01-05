# ⚖️ ASPECTS LÉGAUX - INTERNATIONAL

## ✅ BONNE NOUVELLE: PAS DE BLOCAGE LÉGAL !

Notre software peut être **international dès le Day 1** sans problème légal majeur.

---

## 1. RGPD (GDPR) 🇪🇺

### Ce qui s'applique:
- **RGPD = Standard européen** (et souvent mondial de facto)
- S'applique à TOUS les citoyens UE, peu importe où tu héberges
- Notre stack est déjà RGPD-compliant par design

### Notre conformité:
✅ **Données personnelles** : Email, nom entreprise (c'est tout)
✅ **Consentement** : Opt-in explicite à l'inscription
✅ **Droit à l'oubli** : Soft delete (deleted_at) + hard delete sur demande
✅ **Portabilité** : Export JSON/CSV des données
✅ **Sécurité** : JWT, HTTPS, password hashing (bcrypt)
✅ **DPO** : Pas obligatoire < 250 employés (on est 1-2 personnes)

### Actions requises:
- [ ] Privacy Policy (une pour toute l'Europe, traduire par langue)
- [ ] CGV (une par pays, mais templates similaires)
- [ ] Cookie banner (si on utilise analytics)

**Coût**: 0€ (templates gratuits en ligne) ou 500-1000€ (avocat pour révision)

---

## 2. DONNÉES BANCAIRES

### Ce qu'on NE stocke PAS:
❌ Numéros de carte bancaire
❌ Codes PIN
❌ Identifiants bancaires directs

### Ce qu'on stocke:
✅ Transactions (montants, descriptions) via Bridge API
✅ Factures (créées par l'utilisateur)
✅ IBAN (encrypté) pour affichage uniquement

### Conformité PCI-DSS:
- **PCI-DSS = Pour payment processing** (cartes bancaires)
- **Bridge API = Certifié PCI-DSS** (on délègue)
- **Notre responsabilité** : Ne jamais stocker données cartes
- ✅ On utilise Stripe pour paiements (eux gèrent PCI-DSS)

**Verdict**: ✅ Compliant par design (on ne touche pas aux cartes)

---

## 3. ENTITÉ LÉGALE

### Phase 1-2 (France + Europe): Entité française suffit

**Options**:
1. **Auto-entrepreneur** (simple, jusqu'à ~70K€ CA)
2. **SASU** (recommandé dès 50K€+ CA, plus pro)
3. **SAS** (si duo)

### Pourquoi entité FR suffit pour Europe ?
✅ **UE = Marché unique** : Vendre dans toute l'UE depuis France
✅ **TVA** : Reverse charge (client UE paie TVA de son pays)
✅ **Facturation** : Factures françaises acceptées partout UE
✅ **Banking** : SEPA = unifié dans toute l'UE

### Quand créer entité locale ?
- **Jamais obligatoire en UE** (sauf activité réglementée)
- **Optionnel si gros CA dans 1 pays** (optimisation fiscale)
- **US/CA** : Besoin entité locale (LLC/Corp) si tu veux bank account US

**Coût entité FR**:
- Auto-entrepreneur : 0€
- SASU : ~500€ création + ~300€/an comptable en ligne

---

## 4. COMPTABILITÉ & FISCALITÉ

### Notre software = Outil comptable, pas cabinet comptable

**Ce qu'on fait**:
✅ Automatiser rapprochements bancaires
✅ Catégoriser transactions
✅ Générer rapports

**Ce qu'on ne fait PAS**:
❌ Conseils fiscaux
❌ Déclarations d'impôts
❌ Certification de comptes

### Régulation:
- **Pas de licence nécessaire** (on n'est pas expert-comptable)
- **Disclaimer** : "Outil d'aide, consultez expert-comptable pour décisions fiscales"
- **Partenariats** : Recommander comptables partenaires

### Par pays:
- **France** : OK, pas de licence
- **Belgique** : OK
- **Suisse** : OK
- **UK** : OK
- **Allemagne** : OK (attention Steuerberater = réglementé, mais on ne les remplace pas)

**Verdict**: ✅ Aucune licence nécessaire (on est un outil, pas un service réglementé)

---

## 5. TERMES & CONDITIONS

### CGV par marché:

**Template standard** (adapté par pays):
```
1. Description service
2. Prix et paiement
3. Durée et résiliation
4. Responsabilités
5. Garanties
6. Loi applicable
7. Juridiction compétente
```

**Adaptations par pays**:
- **Loi applicable** : Française si client FR, locale si client autre pays UE
- **Juridiction** : Tribunaux de Paris (ou local selon client)
- **Langue** : Traduire dans langue du client
- **Cooling-off period** : 14 jours (standard UE)

**Coût**:
- Templates gratuits : LegalPlace, Jurismatic
- Révision avocat : 500-1000€ par version

---

## 6. PROPRIÉTÉ INTELLECTUELLE

### Notre code:
✅ **On possède 100% du code**
✅ Pas de dépendances propriétaires
✅ Open-source libraries (MIT/Apache licenses)

### Trademark:
- **"FinanceAI"** : Vérifier disponibilité (INPI France, EUIPO Europe)
- **Coût dépôt** : 
  - France : ~200€
  - Europe (EUIPO) : ~900€
  - International (Madrid) : ~653 CHF + pays

**Recommandation** : Dépôt France maintenant, Europe dans 6 mois si traction

---

## 7. PROTECTION DES DONNÉES PAR PAYS

### RGPD (UE) 🇪🇺
✅ On est compliant

### UK GDPR 🇬🇧
✅ Quasi-identique au RGPD UE

### CCPA (Californie, US) 🇺🇸
- S'applique si clients Californiens
- Similaire à RGPD
- ✅ Notre conformité RGPD couvre 90% des exigences

### Autres pays:
- **Canada (PIPEDA)** : Similaire RGPD
- **Suisse (LPD)** : Similaire RGPD (mais hors UE)
- **Brésil (LGPD)** : Inspiré du RGPD

**Verdict**: ✅ RGPD = Gold standard, couvre la majorité des juridictions

---

## 8. HÉBERGEMENT & SOUVERAINETÉ DES DONNÉES

### Où héberger ?

**Recommandation**: 🇪🇺 **Europe**

**Options**:
1. **Supabase** (EU region: Frankfurt) ✅
2. **Railway** (EU region available) ✅
3. **Fly.io** (EU regions) ✅
4. **OVH** (français, RGPD natif) ✅

### Pourquoi Europe ?
✅ RGPD compliant par défaut
✅ Pas de Schrems II issues (US transfers)
✅ Argument commercial (données en Europe)

### Si clients US/CA ?
- OK héberger en Europe
- Ou dupliquer infra en US (plus tard)

---

## 9. ANTI-BLANCHIMENT (AML) / KYC

### Notre cas:
- **On ne fait PAS de transferts d'argent**
- **On ne touchons PAS aux fonds clients**
- **Bridge API** = Eux gèrent AML/KYC

### Obligations:
❌ Pas de KYC obligatoire (on n'est pas PSP/banque)
✅ Mais good practice : Vérifier email, entreprise réelle

### Si on ajoutait paiements clients plus tard:
- Utiliser Stripe (eux gèrent AML)
- Ou Mangopay (français, pour marketplace)

**Verdict**: ✅ Pas d'obligation AML (on ne manipule pas de fonds)

---

## 10. CHECKLIST LÉGALE PAR PHASE

### Phase 1: MVP (Mois 1-6) 🇫🇷

**Obligatoire**:
- [ ] Créer entité (SASU recommandé)
- [ ] Privacy Policy (FR, puis traduire)
- [ ] CGV (FR)
- [ ] Mentions légales site
- [ ] Cookie banner (si analytics)
- [ ] RGPD: Consentement + Droit à l'oubli

**Budget**: 500-1000€

---

### Phase 2: Expansion Europe (Mois 7-12) 🇪🇺

**Obligatoire**:
- [ ] Traduire Privacy Policy (EN, NL, DE, etc.)
- [ ] Adapter CGV par pays (loi applicable)
- [ ] Dépôt trademark EUIPO (optionnel mais recommandé)

**Budget**: +500-1000€

---

### Phase 3: International (Mois 13+) 🌍

**Si UK**:
- [ ] UK GDPR compliance check
- [ ] UK entity (optionnel)

**Si US/CA**:
- [ ] CCPA compliance (Californie)
- [ ] US entity (LLC Delaware/Wyoming)
- [ ] US bank account

**Budget**: +2000-5000€

---

## ✅ CONCLUSION

### Réponse à ta question: **OUI, international-ready Day 1 est légal ! 🎉**

**Ce qui est déjà OK**:
✅ RGPD compliant par design
✅ Pas de licence nécessaire
✅ Entité FR suffit pour UE
✅ Bridge API gère PCI-DSS/AML
✅ Hébergement EU = compliant

**Ce qu'il faut faire (obligatoire)**:
1. Privacy Policy (1 jour, templates gratuits)
2. CGV (1 jour, templates gratuits)
3. Mentions légales (1 heure)
4. Créer entité (SASU: 1 semaine)

**Coût total Phase 1**: 500-1000€
**Temps setup légal**: 1-2 jours

**Bloqueurs légaux**: ✅ **AUCUN**

---

## 📋 TODO AVANT LANCEMENT

### Maintenant (Mois 1):
```bash
# 1. Templates légaux (gratuit)
- Privacy Policy: https://www.privacypolicies.com/
- CGV SaaS: https://www.legalplace.fr/
- RGPD: https://www.cnil.fr/

# 2. Créer entité
- SASU: https://www.legalstart.fr/ (~500€)
- Ou auto-entrepreneur: https://www.autoentrepreneur.urssaf.fr/ (gratuit)

# 3. Site
- Ajouter /legal/privacy
- Ajouter /legal/terms
- Ajouter /legal/mentions-legales
- Cookie banner: https://www.cookiebot.com/ (free tier)
```

### Avant premier client payant:
- [ ] Stripe account vérifié
- [ ] CGV signées électroniquement
- [ ] Factures automatiques (Stripe gère)
- [ ] Assurance RC Pro (optionnel, ~300€/an)

---

**TU ES GOOD TO GO! 🚀** Aucun blocage légal pour être international-ready dès maintenant.

