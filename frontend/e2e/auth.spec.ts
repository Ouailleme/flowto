import { test, expect } from '@playwright/test';

const TEST_USER = {
  email: 'test-e2e@financeai.com',
  password: 'TestPassword123!',
  fullName: 'Test E2E User',
};

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display landing page', async ({ page }) => {
    await expect(page).toHaveTitle(/FinanceAI/);
    await expect(page.locator('h1')).toContainText('Automatisez votre');
    
    // Check CTA buttons
    await expect(page.getByRole('link', { name: /commencer gratuitement/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /découvrir/i })).toBeVisible();
  });

  test('should navigate to login page', async ({ page }) => {
    await page.getByRole('link', { name: /commencer gratuitement/i }).click();
    
    // Should redirect to login or register
    await expect(page).toHaveURL(/\/(auth\/login|auth\/register)/);
  });

  test('should show validation errors on empty login form', async ({ page }) => {
    await page.goto('/auth/login');
    
    // Try to submit empty form
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    // HTML5 validation should prevent submission
    const emailInput = page.getByLabel(/email/i);
    await expect(emailInput).toHaveAttribute('required');
  });

  test('should login with demo account', async ({ page }) => {
    await page.goto('/auth/login');
    
    // Fill credentials
    await page.getByLabel(/email/i).fill('demo@financeai.com');
    await page.getByLabel(/mot de passe/i).fill('Demo2026!');
    
    // Submit
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Check dashboard loaded
    await expect(page.locator('h1')).toContainText(/bonjour|tableau de bord/i);
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await page.goto('/auth/login');
    
    await page.getByLabel(/email/i).fill('wrong@email.com');
    await page.getByLabel(/mot de passe/i).fill('wrongpassword');
    
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    // Should show error toast or message
    await expect(page.locator('text=/erreur|incorrect/i')).toBeVisible({ timeout: 5000 });
  });

  test('should navigate to register page', async ({ page }) => {
    await page.goto('/auth/login');
    
    await page.getByRole('link', { name: /créer un compte/i }).click();
    
    await expect(page).toHaveURL('/auth/register');
    await expect(page.locator('h2')).toContainText(/créer un compte/i);
  });

  test('should show password mismatch error', async ({ page }) => {
    await page.goto('/auth/register');
    
    await page.getByLabel(/nom complet/i).fill(TEST_USER.fullName);
    await page.getByLabel(/email/i).fill(TEST_USER.email);
    await page.getByLabel('Mot de passe').fill(TEST_USER.password);
    await page.getByLabel(/confirmer/i).fill('DifferentPassword123!');
    
    await page.getByRole('button', { name: /créer mon compte/i }).click();
    
    // Should show mismatch alert
    page.once('dialog', dialog => {
      expect(dialog.message()).toContain('ne correspondent pas');
      dialog.accept();
    });
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await page.goto('/auth/login');
    await page.getByLabel(/email/i).fill('demo@financeai.com');
    await page.getByLabel(/mot de passe/i).fill('Demo2026!');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Logout
    await page.getByRole('button', { name: /déconnexion/i }).click();
    
    // Should redirect to login
    await expect(page).toHaveURL('/auth/login', { timeout: 5000 });
  });
});

