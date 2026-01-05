import { test, expect } from '@playwright/test';

/**
 * Complete E2E flow testing:
 * 1. Login
 * 2. View dashboard
 * 3. Create invoice
 * 4. View transactions
 * 5. Categorize transaction
 * 6. Navigate to settings
 * 7. Logout
 */
test.describe('Complete User Flow', () => {
  test('should complete full user journey', async ({ page }) => {
    // Step 1: Login
    await page.goto('/auth/login');
    await page.getByLabel(/email/i).fill('demo@financeai.com');
    await page.getByLabel(/mot de passe/i).fill('Demo2026!');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
    console.log('✅ Step 1: Login successful');
    
    // Step 2: View dashboard
    await expect(page.locator('h1')).toContainText(/bonjour/i);
    await expect(page.getByText(/factures en attente/i)).toBeVisible();
    console.log('✅ Step 2: Dashboard loaded');
    
    // Step 3: Navigate to invoices and create new invoice
    await page.getByRole('link', { name: /^factures$/i }).click();
    await expect(page).toHaveURL('/dashboard/invoices');
    
    await page.getByRole('link', { name: /nouvelle facture/i }).click();
    await expect(page).toHaveURL('/dashboard/invoices/new');
    
    const timestamp = Date.now();
    await page.getByLabel(/nom du client/i).fill(`E2E Client ${timestamp}`);
    await page.getByLabel(/email/i).fill(`e2e${timestamp}@test.com`);
    await page.getByLabel(/montant ht/i).fill('500');
    await page.getByLabel(/tva/i).fill('100');
    
    await page.getByRole('button', { name: /créer la facture/i }).click();
    
    await expect(page).toHaveURL('/dashboard/invoices', { timeout: 10000 });
    console.log('✅ Step 3: Invoice created');
    
    // Step 4: View transactions
    await page.getByRole('link', { name: /^transactions$/i }).click();
    await expect(page).toHaveURL('/dashboard/transactions');
    
    await expect(page.getByRole('table')).toBeVisible({ timeout: 5000 });
    console.log('✅ Step 4: Transactions loaded');
    
    // Step 5: Bulk categorize transactions
    const bulkButton = page.getByRole('button', { name: /catégoriser tout/i });
    if (await bulkButton.isVisible()) {
      await bulkButton.click();
      await page.waitForTimeout(3000); // Wait for categorization
      console.log('✅ Step 5: Transactions categorized');
    }
    
    // Step 6: Navigate to settings
    await page.getByRole('link', { name: /paramètres/i }).click();
    await expect(page).toHaveURL('/dashboard/settings');
    
    await expect(page.locator('h1')).toContainText(/paramètres/i);
    console.log('✅ Step 6: Settings page loaded');
    
    // Step 7: Back to dashboard
    await page.getByRole('link', { name: /tableau de bord/i }).click();
    await expect(page).toHaveURL('/dashboard');
    console.log('✅ Step 7: Back to dashboard');
    
    // Step 8: Logout
    await page.getByRole('button', { name: /déconnexion/i }).click();
    await expect(page).toHaveURL('/auth/login', { timeout: 5000 });
    console.log('✅ Step 8: Logout successful');
    
    console.log('🎉 Complete flow finished successfully!');
  });
});

