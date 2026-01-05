import { test, expect } from '@playwright/test';

test.describe('Settings', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/auth/login');
    await page.getByLabel(/email/i).fill('demo@financeai.com');
    await page.getByLabel(/mot de passe/i).fill('Demo2026!');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Navigate to settings
    await page.getByRole('link', { name: /paramètres/i }).click();
    await expect(page).toHaveURL('/dashboard/settings');
  });

  test('should display settings page', async ({ page }) => {
    await expect(page.locator('h1')).toContainText(/paramètres/i);
  });

  test('should display profile section', async ({ page }) => {
    await expect(page.getByText(/profil/i).first()).toBeVisible();
    
    // Email should be displayed and disabled
    const emailInput = page.getByLabel(/email/i);
    await expect(emailInput).toBeVisible();
    await expect(emailInput).toBeDisabled();
    await expect(emailInput).toHaveValue('demo@financeai.com');
  });

  test('should display localization section', async ({ page }) => {
    await expect(page.getByText(/localisation/i).first()).toBeVisible();
    
    // Should have language dropdown
    const languageSelect = page.locator('select#language');
    await expect(languageSelect).toBeVisible();
    
    // Should have currency dropdown
    const currencySelect = page.locator('select#currency');
    await expect(currencySelect).toBeVisible();
  });

  test('should display subscription section', async ({ page }) => {
    await expect(page.getByText(/abonnement/i).first()).toBeVisible();
    
    // Should show current plan
    await expect(page.getByText(/plan actuel/i)).toBeVisible();
    await expect(page.getByText(/essai gratuit/i)).toBeVisible();
  });

  test('should display notification settings', async ({ page }) => {
    await expect(page.getByText(/notifications/i).first()).toBeVisible();
    
    // Should have checkboxes
    const checkboxes = page.locator('input[type="checkbox"]');
    expect(await checkboxes.count()).toBeGreaterThan(0);
  });

  test('should display danger zone', async ({ page }) => {
    await expect(page.getByText(/zone de danger/i)).toBeVisible();
    await expect(page.getByText(/supprimer le compte/i)).toBeVisible();
    
    // Delete button should be visible
    const deleteButton = page.getByRole('button', { name: /supprimer/i });
    await expect(deleteButton).toBeVisible();
  });

  test('should have save buttons', async ({ page }) => {
    // Multiple save buttons throughout the page
    const saveButtons = page.getByRole('button', { name: /sauvegarder/i });
    expect(await saveButtons.count()).toBeGreaterThan(0);
  });
});

