# Tests - FinanceAI

Tests complets avec **90%+ coverage** obligatoire.

## 🧪 Structure

```
tests/
├── conftest.py              # Fixtures pytest globales
├── unit/                    # Tests unitaires (services, utils)
│   └── services/
│       ├── test_auth_service.py
│       ├── test_bank_service.py
│       ├── test_invoice_service.py
│       └── test_transaction_service.py
├── integration/             # Tests d'intégration (API + DB)
│   ├── test_auth_api.py
│   ├── test_banks_api.py
│   ├── test_invoices_api.py
│   └── test_transactions_api.py
└── e2e/                     # Tests end-to-end (flows complets)
    └── test_reconciliation_flow.py
```

## 🚀 Lancer les tests

### Tous les tests
```bash
cd backend
pytest
```

### Tests unitaires uniquement
```bash
pytest tests/unit
```

### Tests d'intégration uniquement
```bash
pytest tests/integration
```

### Avec coverage détaillé
```bash
pytest --cov=app --cov-report=html
# Ouvrir htmlcov/index.html dans un navigateur
```

### Tests spécifiques
```bash
# Un fichier
pytest tests/unit/services/test_bank_service.py

# Une classe
pytest tests/unit/services/test_bank_service.py::TestBankService

# Un test
pytest tests/unit/services/test_bank_service.py::TestBankService::test_create_bank_account
```

### Avec markers
```bash
# Tests unitaires uniquement
pytest -m unit

# Tests d'intégration uniquement
pytest -m integration

# Exclure tests lents
pytest -m "not slow"
```

## 📋 Fixtures disponibles

### Database
- `db_session`: Session async PostgreSQL pour tests
- `setup_database`: Setup/teardown automatique de la DB

### Users
- `test_user`: Utilisateur test par défaut
- `test_user_2`: Second utilisateur pour tests d'isolation

### Auth
- `auth_token`: JWT token pour `test_user`
- `auth_headers`: Headers HTTP avec token (`Authorization: Bearer ...`)

### Client
- `client`: AsyncClient HTTP pour tester l'API

### Factories
- `invoice_factory()`: Génère données invoice test
- `bank_account_factory()`: Génère données bank account test
- `transaction_factory()`: Génère données transaction test

## ✅ Bonnes pratiques

1. **Un test = une fonctionnalité**
   ```python
   async def test_create_invoice_with_valid_data():
       # Arrange
       data = invoice_factory()
       
       # Act
       invoice = await InvoiceService.create(db, user_id, data)
       
       # Assert
       assert invoice.id is not None
       assert invoice.status == "pending"
   ```

2. **Tester les cas d'erreur**
   ```python
   async def test_create_invoice_duplicate_number():
       with pytest.raises(ValueError, match="already exists"):
           await InvoiceService.create(db, user_id, data)
   ```

3. **Tester l'isolation entre users**
   ```python
   async def test_user_cannot_access_other_user_invoice():
       invoice = await InvoiceService.create(db, user1_id, data)
       
       retrieved = await InvoiceService.get(db, invoice.id, user2_id)
       assert retrieved is None
   ```

4. **Noms de tests descriptifs**
   - ✅ `test_create_invoice_with_past_due_date_sets_overdue_status`
   - ❌ `test_invoice_1`

5. **Utiliser les markers**
   ```python
   @pytest.mark.slow
   @pytest.mark.integration
   async def test_full_reconciliation_flow():
       ...
   ```

## 📊 Coverage cible

- **Global**: 90%+ obligatoire
- **Services**: 95%+
- **API endpoints**: 90%+
- **Models**: 80%+

## 🐛 Débugger les tests

```bash
# Mode verbose
pytest -vv

# Stopper au premier échec
pytest -x

# Afficher print statements
pytest -s

# Avec debugger
pytest --pdb

# Lancer uniquement les tests qui ont échoué
pytest --lf
```

## 🔄 CI/CD

Les tests sont automatiquement lancés sur chaque PR via GitHub Actions.

Le build échoue si:
- Coverage < 90%
- Tests échouent
- Linter errors

---

**Tests = sécurité et confiance !** 🛡️


