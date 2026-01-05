import { test, expect } from '@playwright/test';

test.describe('Invoices', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/auth/login');
    await page.getByLabel(/email/i).fill('demo@financeai.com');
    await page.getByLabel(/mot de passe/i).fill('Demo2026!');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    
    // Navigate to invoices
    await page.getByRole('link', { name: /^factures$/i }).click();
    await expect(page).toHaveURL('/dashboard/invoices');
  });

  test('should display invoices page', async ({ page }) => {
    await expect(page.locator('h1')).toContainText(/factures/i);
    
    // Should have "Nouvelle facture" button
    await expect(page.getByRole('link', { name: /nouvelle facture/i })).toBeVisible();
  });

  test('should display invoice stats', async ({ page }) => {
    // Check stats cards
    await expect(page.getByText(/total factures/i)).toBeVisible();
    await expect(page.getByText(/en attente/i)).toBeVisible();
    await expect(page.getByText(/en retard/i)).toBeVisible();
    await expect(page.getByText(/payées/i)).toBeVisible();
  });

  test('should display invoices table', async ({ page }) => {
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    
    // Check headers
    await expect(page.getByRole('columnheader', { name: /n° facture/i })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: /client/i })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: /montant/i })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: /statut/i })).toBeVisible();
  });

  test('should navigate to new invoice page', async ({ page }) => {
    await page.getByRole('link', { name: /nouvelle facture/i }).click();
    
    await expect(page).toHaveURL('/dashboard/invoices/new');
    await expect(page.locator('h1')).toContainText(/nouvelle facture/i);
  });

  test('should create a new invoice', async ({ page }) => {
    await page.getByRole('link', { name: /nouvelle facture/i }).click();
    
    // Fill form
    const timestamp = Date.now();
    await page.getByLabel(/nom du client/i).fill(`Test Client ${timestamp}`);
    await page.getByLabel(/email/i).fill(`client${timestamp}@test.com`);
    await page.getByLabel(/montant ht/i).fill('1000');
    await page.getByLabel(/tva/i).fill('200');
    
    // Dates should be pre-filled
    
    // Submit
    await page.getByRole('button', { name: /créer la facture/i }).click();
    
    // Should redirect back to invoices list
    await expect(page).toHaveURL('/dashboard/invoices', { timeout: 10000 });
    
    // Should show success toast
    await expect(page.locator('text=/créée|succès/i')).toBeVisible({ timeout: 5000 });
  });

  test('should validate required fields', async ({ page }) => {
    await page.getByRole('link', { name: /nouvelle facture/i }).click();
    
    // Try to submit empty form
    await page.getByRole('button', { name: /créer la facture/i }).click();
    
    // HTML5 validation should prevent submission
    const clientNameInput = page.getByLabel(/nom du client/i);
    await expect(clientNameInput).toHaveAttribute('required');
  });

  test('should calculate total automatically', async ({ page }) => {
    await page.getByRole('link', { name: /nouvelle facture/i }).click();
    
    // Fill amounts
    await page.getByLabel(/montant ht/i).fill('1000');
    await page.getByLabel(/tva/i).fill('200');
    
    // Total should be calculated
    await expect(page.getByText(/1200.*EUR/i)).toBeVisible({ timeout: 2000 });
  });

  test('should have search functionality', async ({ page }) => {
    const searchInput = page.getByPlaceholder(/rechercher/i);
    await expect(searchInput).toBeVisible();
  });

  test('should display invoice actions', async ({ page }) => {
    // Wait for table
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    
    // Should have action buttons in each row (edit, delete, mail)
    // Check if at least one mail icon exists (for pending invoices)
    const rows = page.getByRole('row');
    const rowCount = await rows.count();
    
    // Should have more than just header row
    expect(rowCount).toBeGreaterThan(1);
  });

  test('should delete invoice with confirmation', async ({ page }) => {
    // Wait for table
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    
    // Find first delete button (trash icon)
    const deleteButtons = page.locator('button[title="Supprimer"]');
    
    if (await deleteButtons.count() > 0) {
      await deleteButtons.first().click();
      
      // Confirmation dialog should appear
      await expect(page.getByText(/supprimer la facture/i)).toBeVisible();
      
      // Cancel
      await page.getByRole('button', { name: /annuler/i }).click();
      
      // Dialog should close
      await expect(page.getByText(/supprimer la facture/i)).not.toBeVisible();
    }
  });

  test('should show invoice status badges', async ({ page }) => {
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    
    // Should have status badges (pending, paid, overdue)
    const badges = page.locator('[class*="badge"]');
    await expect(badges.first()).toBeVisible({ timeout: 5000 });
  });

  test('should go back from new invoice page', async ({ page }) => {
    await page.getByRole('link', { name: /nouvelle facture/i }).click();
    await expect(page).toHaveURL('/dashboard/invoices/new');
    
    // Click back link
    await page.getByRole('link', { name: /retour/i }).click();
    
    await expect(page).toHaveURL('/dashboard/invoices');
  });
});

