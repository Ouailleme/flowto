# 🧪 Tests E2E - FinanceAI

Tests End-to-End automatisés avec **Playwright**.

## 📋 Tests Couverts

### **1. Authentication (`auth.spec.ts`)**
✅ Display landing page
✅ Navigate to login/register
✅ Login with demo account
✅ Show error on invalid credentials
✅ Register new user
✅ Password validation
✅ Logout

### **2. Dashboard (`dashboard.spec.ts`)**
✅ Display stats cards
✅ Display recent invoices/transactions
✅ Quick actions visible
✅ Navigation to all pages
✅ Sidebar navigation
✅ User info displayed

### **3. Transactions (`transactions.spec.ts`)**
✅ Display transactions table
✅ Search functionality
✅ Bulk categorization
✅ Export button
✅ Category badges
✅ Pagination
✅ Individual categorization

### **4. Invoices (`invoices.spec.ts`)**
✅ Display invoices table
✅ Create new invoice
✅ Form validation
✅ Auto-calculate total
✅ Search functionality
✅ Delete with confirmation
✅ Status badges

### **5. Settings (`settings.spec.ts`)**
✅ Display all sections
✅ Profile section
✅ Localization (language, currency)
✅ Subscription info
✅ Notification settings
✅ Danger zone

### **6. Complete Flow (`complete-flow.spec.ts`)**
✅ Full user journey (8 steps)
- Login → Dashboard → Create Invoice → Transactions → Categorize → Settings → Logout

---

## 🚀 Installation

```bash
cd frontend

# Installer Playwright
npm install -D @playwright/test

# Installer les browsers
npx playwright install
```

---

## 🧪 Lancer les Tests

### **Tous les tests**
```bash
npm run test:e2e
```

### **Mode UI (recommandé pour debug)**
```bash
npm run test:e2e:ui
```

### **Mode headed (voir le navigateur)**
```bash
npm run test:e2e:headed
```

### **Mode debug (step-by-step)**
```bash
npm run test:e2e:debug
```

### **Tests spécifiques**
```bash
# Un fichier
npx playwright test e2e/auth.spec.ts

# Un test spécifique
npx playwright test -g "should login with demo account"

# Un browser spécifique
npx playwright test --project=chromium
```

---

## 📊 Rapport de Tests

### **Générer le rapport**
```bash
npm run test:e2e
```

### **Voir le rapport HTML**
```bash
npm run test:e2e:report
```

Le rapport s'ouvre automatiquement dans le navigateur avec:
- ✅ Tests passés / échoués
- 📸 Screenshots des erreurs
- 🎥 Vidéos des tests échoués
- 📍 Traces complètes

---

## 🎯 Browsers Testés

- ✅ **Chromium** (Chrome/Edge)
- ✅ **Firefox**
- ✅ **WebKit** (Safari)
- ✅ **Mobile Chrome** (Pixel 5)
- ✅ **Mobile Safari** (iPhone 12)

---

## 🔧 Configuration

Voir `playwright.config.ts` pour:
- Base URL
- Timeouts
- Retry logic
- Screenshots/videos
- Browsers

---

## 📝 Écrire de Nouveaux Tests

```typescript
import { test, expect } from '@playwright/test';

test.describe('Ma Feature', () => {
  test.beforeEach(async ({ page }) => {
    // Setup avant chaque test
    await page.goto('/auth/login');
    // Login, etc.
  });

  test('should do something', async ({ page }) => {
    // Arrange
    await page.goto('/my-page');
    
    // Act
    await page.getByRole('button', { name: /click me/i }).click();
    
    // Assert
    await expect(page.locator('h1')).toContainText('Success');
  });
});
```

---

## 🐛 Debugging

### **Playwright Inspector**
```bash
npx playwright test --debug
```

### **Pause dans un test**
```typescript
await page.pause();
```

### **Screenshots**
```typescript
await page.screenshot({ path: 'screenshot.png' });
```

### **Console logs**
```typescript
page.on('console', msg => console.log(msg.text()));
```

---

## ✅ Best Practices

### **1. Sélecteurs Stables**
```typescript
// ✅ GOOD - Rôle ARIA
await page.getByRole('button', { name: /submit/i });

// ❌ BAD - Classes CSS
await page.locator('.btn-submit');
```

### **2. Attendre les éléments**
```typescript
// ✅ GOOD
await expect(page.locator('h1')).toBeVisible({ timeout: 5000 });

// ❌ BAD
await page.waitForTimeout(5000);
```

### **3. Isolation des tests**
```typescript
// Chaque test doit être indépendant
test.beforeEach(async ({ page }) => {
  // Fresh login pour chaque test
});
```

### **4. Noms descriptifs**
```typescript
// ✅ GOOD
test('should create invoice with valid data', ...)

// ❌ BAD
test('test1', ...)
```

---

## 🚨 Troubleshooting

### **Tests timeout**
```typescript
// Augmenter timeout
test('slow test', async ({ page }) => {
  test.setTimeout(60000); // 60 seconds
  ...
});
```

### **Backend pas lancé**
```bash
# S'assurer que le backend tourne
cd backend
uvicorn app.main:app --reload

# Playwright lancera automatiquement le frontend
```

### **Browsers pas installés**
```bash
npx playwright install
```

### **Tests flaky**
```typescript
// Ajouter retry
test.describe.configure({ mode: 'parallel', retries: 2 });
```

---

## 📈 CI/CD

### **GitHub Actions**
```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 🎉 Résultats Attendus

Avec tous les tests passants:
```
Running 45 tests using 5 workers

  ✓ auth.spec.ts:12:3 › Authentication Flow › should display landing page
  ✓ auth.spec.ts:18:3 › Authentication Flow › should navigate to login page
  ✓ auth.spec.ts:25:3 › Authentication Flow › should login with demo account
  ...
  ✓ complete-flow.spec.ts:10:3 › Complete User Flow › should complete full user journey

  45 passed (2.5m)
```

---

## 📚 Documentation Playwright

- **Docs**: https://playwright.dev/docs/intro
- **API**: https://playwright.dev/docs/api/class-playwright
- **Best Practices**: https://playwright.dev/docs/best-practices

---

**🎉 Tests E2E complets pour FinanceAI ! 🚀**

**Tous les flows critiques sont couverts automatiquement !**


