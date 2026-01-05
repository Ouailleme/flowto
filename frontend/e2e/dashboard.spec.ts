import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/auth/login');
    await page.getByLabel(/email/i).fill('demo@financeai.com');
    await page.getByLabel(/mot de passe/i).fill('Demo2026!');
    await page.getByRole('button', { name: /se connecter/i }).click();
    
    await expect(page).toHaveURL('/dashboard', { timeout: 10000 });
  });

  test('should display dashboard with stats', async ({ page }) => {
    // Check title
    await expect(page.locator('h1')).toContainText(/bonjour/i);
    
    // Check stats cards are visible
    await expect(page.getByText(/factures en attente/i)).toBeVisible();
    await expect(page.getByText(/factures en retard/i)).toBeVisible();
    await expect(page.getByText(/transactions ce mois/i)).toBeVisible();
  });

  test('should display recent invoices', async ({ page }) => {
    await expect(page.getByText(/factures récentes/i)).toBeVisible();
    
    // Should have "Voir tout" link
    const viewAllLink = page.getByRole('link', { name: /voir tout/i }).first();
    await expect(viewAllLink).toBeVisible();
  });

  test('should display recent transactions', async ({ page }) => {
    await expect(page.getByText(/transactions récentes/i)).toBeVisible();
  });

  test('should have quick actions', async ({ page }) => {
    await expect(page.getByText(/actions rapides/i)).toBeVisible();
    
    // Check action cards
    await expect(page.getByText(/créer une facture/i)).toBeVisible();
    await expect(page.getByText(/catégoriser/i)).toBeVisible();
    await expect(page.getByText(/rapprochements/i)).toBeVisible();
  });

  test('should navigate to transactions page', async ({ page }) => {
    await page.getByRole('link', { name: /^transactions$/i }).click();
    
    await expect(page).toHaveURL('/dashboard/transactions');
    await expect(page.locator('h1')).toContainText(/transactions/i);
  });

  test('should navigate to invoices page', async ({ page }) => {
    await page.getByRole('link', { name: /^factures$/i }).click();
    
    await expect(page).toHaveURL('/dashboard/invoices');
    await expect(page.locator('h1')).toContainText(/factures/i);
  });

  test('should navigate to settings page', async ({ page }) => {
    await page.getByRole('link', { name: /paramètres/i }).click();
    
    await expect(page).toHaveURL('/dashboard/settings');
    await expect(page.locator('h1')).toContainText(/paramètres/i);
  });

  test('should have sidebar navigation', async ({ page }) => {
    const sidebar = page.locator('aside');
    
    // Check logo
    await expect(sidebar.getByText(/financeai/i)).toBeVisible();
    
    // Check nav links
    await expect(sidebar.getByRole('link', { name: /tableau de bord/i })).toBeVisible();
    await expect(sidebar.getByRole('link', { name: /transactions/i })).toBeVisible();
    await expect(sidebar.getByRole('link', { name: /factures/i })).toBeVisible();
  });

  test('should display user info in sidebar', async ({ page }) => {
    const sidebar = page.locator('aside');
    
    // Should show email
    await expect(sidebar.getByText(/demo@financeai.com/i)).toBeVisible();
  });
});

