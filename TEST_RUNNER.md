# 🧪 Guide pour Lancer les Tests

## 🚀 DÉMARRAGE RAPIDE (Copier-coller ces commandes)

### **Étape 1: Lancer les services Docker**
```bash
# Depuis la racine du projet
docker-compose up -d
```

### **Étape 2: Lancer le Backend (Terminal 1)**
```bash
cd backend

# Créer venv si pas encore fait
python -m venv venv

# Activer venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Installer dependencies
pip install -r requirements.txt

# Créer .env
copy .env.example .env
# Puis éditer .env avec un éditeur

# Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Étape 3: Lancer le Frontend (Terminal 2)**
```bash
cd frontend

# Si pas déjà fait
npm install

# Créer .env.local
copy .env.local.example .env.local

# Lancer dev server
npm run dev
```

### **Étape 4: Lancer les Tests E2E (Terminal 3)**
```bash
cd frontend

# Mode UI (recommandé)
npm run test:e2e:ui

# OU mode normal
npm run test:e2e

# OU mode headed (voir le browser)
npm run test:e2e:headed
```

---

## ✅ CHECKLIST PRÉ-TESTS

- [ ] Docker running (PostgreSQL + Redis)
- [ ] Backend running sur http://localhost:8000
- [ ] Frontend running sur http://localhost:3000
- [ ] `.env` créé dans `backend/`
- [ ] `.env.local` créé dans `frontend/`

---

## 🎯 COMMANDES TESTS

```bash
# Tous les tests
npm run test:e2e

# Mode UI (meilleur pour debug)
npm run test:e2e:ui

# Mode headed (voir navigateur)
npm run test:e2e:headed

# Debug mode (step-by-step)
npm run test:e2e:debug

# Un fichier spécifique
npx playwright test e2e/auth.spec.ts

# Un test spécifique
npx playwright test -g "should login with demo account"

# Voir le rapport
npm run test:e2e:report
```

---

## 🐛 TROUBLESHOOTING

### **Backend ne démarre pas**
```bash
# Vérifier PostgreSQL
docker-compose ps

# Recréer la DB
docker-compose down -v
docker-compose up -d
```

### **Frontend ne démarre pas**
```bash
# Réinstaller
rm -rf node_modules package-lock.json
npm install
```

### **Tests timeout**
```bash
# Vérifier que backend ET frontend tournent
curl http://localhost:8000/health
curl http://localhost:3000
```

### **Port déjà utilisé**
```powershell
# Windows: Tuer processus sur port
netstat -ano | findstr :8000
taskkill /PID <PID> /F

netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

## 📊 RÉSULTAT ATTENDU

```
Running 45 tests using 5 workers

  ✓ e2e/auth.spec.ts (8/8)
  ✓ e2e/dashboard.spec.ts (8/8)
  ✓ e2e/transactions.spec.ts (10/10)
  ✓ e2e/invoices.spec.ts (12/12)
  ✓ e2e/settings.spec.ts (7/7)
  ✓ e2e/complete-flow.spec.ts (1/1)

  45 passed (4.2m)
```

---

## 🎉 C'EST TOUT !

Une fois les 3 services lancés (Docker, Backend, Frontend), les tests devraient passer à 100% ! 🚀


