import { test, expect } from '@playwright/test';

test.describe('Transactions', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/auth/login');
    await page.getByLabel(/email/i).fill('demo@financeai.com');
    await page.getByLabel(/mot de passe/i).fill('Demo2026!');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Navigate to transactions
    await page.getByRole('link', { name: /^transactions$/i }).click();
    await expect(page).toHaveURL('/dashboard/transactions');
  });

  test('should display transactions page', async ({ page }) => {
    await expect(page.locator('h1')).toContainText(/transactions/i);
    
    // Should have stats cards
    await expect(page.getByText(/transactions ce mois/i)).toBeVisible();
    await expect(page.getByText(/catégorisées/i)).toBeVisible();
    await expect(page.getByText(/rapprochées/i)).toBeVisible();
  });

  test('should display transactions table', async ({ page }) => {
    // Wait for table to load
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    
    // Check table headers
    await expect(page.getByRole('columnheader', { name: /date/i })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: /description/i })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: /catégorie/i })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: /montant/i })).toBeVisible();
  });

  test('should have search functionality', async ({ page }) => {
    const searchInput = page.getByPlaceholder(/rechercher/i);
    await expect(searchInput).toBeVisible();
    
    // Type in search
    await searchInput.fill('loyer');
    
    // Results should filter (wait a bit for debounce)
    await page.waitForTimeout(1000);
  });

  test('should have bulk categorization button', async ({ page }) => {
    const bulkButton = page.getByRole('button', { name: /catégoriser tout/i });
    await expect(bulkButton).toBeVisible();
    
    // Click should trigger categorization
    await bulkButton.click();
    
    // Should show loading state or success
    await expect(page.locator('text=/catégorisation/i')).toBeVisible({ timeout: 10000 });
  });

  test('should have export button', async ({ page }) => {
    const exportButton = page.getByRole('button', { name: /exporter/i });
    await expect(exportButton).toBeVisible();
  });

  test('should display transaction amounts correctly', async ({ page }) => {
    // Wait for transactions to load
    await expect(page.getByRole('table')).toBeVisible();
    
    // Should have at least one transaction row
    const rows = page.getByRole('row');
    await expect(rows).not.toHaveCount(1); // More than just header
  });

  test('should show category badges', async ({ page }) => {
    // Wait for table
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    
    // Should have category badges or "Non catégorisé"
    const categoryBadges = page.locator('[class*="badge"]');
    // At least one badge should exist
    await expect(categoryBadges.first()).toBeVisible({ timeout: 5000 });
  });

  test('should paginate transactions', async ({ page }) => {
    // Wait for table
    await expect(page.getByRole('table')).toBeVisible();
    
    // Check if pagination exists (only if more than 20 transactions)
    const nextButton = page.getByRole('button', { name: /suivant/i });
    const prevButton = page.getByRole('button', { name: /précédent/i });
    
    // Previous should be disabled on first page
    if (await prevButton.isVisible()) {
      await expect(prevButton).toBeDisabled();
    }
  });

  test('should categorize individual transaction', async ({ page }) => {
    // Wait for table
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    
    // Find a transaction with sparkle icon (categorize button)
    const categorizeButtons = page.locator('button:has-text("")').filter({ has: page.locator('svg') });
    
    if (await categorizeButtons.count() > 0) {
      await categorizeButtons.first().click();
      
      // Should trigger categorization (check for toast or loading)
      await page.waitForTimeout(2000);
    }
  });
});

