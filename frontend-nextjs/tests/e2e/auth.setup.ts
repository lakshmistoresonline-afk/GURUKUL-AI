import { test as setup, expect } from '@playwright/test';
import { STORAGE_STATE } from '../../playwright.config';

setup('authenticate', async ({ page }) => {
  const username = process.env.TEST_USERNAME || 'tester_v1';
  const password = process.env.TEST_PASSWORD;

  if (!password) {
    throw new Error(
      'TEST_PASSWORD environment variable is required for E2E authentication.'
    );
  }

  await page.goto('/');

  // Wait for the login form heading to render
  await expect(
    page.getByRole('heading', { name: 'Student Login' })
  ).toBeVisible({ timeout: 30000 });

  const usernameInput = page.locator('input[type="text"]').first();
  const passwordInput = page.locator('input[type="password"]').first();

  await expect(usernameInput).toBeVisible({ timeout: 30000 });
  await expect(passwordInput).toBeVisible({ timeout: 30000 });

  await usernameInput.fill(username);
  await passwordInput.fill(password);

  const loginButton = page.getByRole('button', { name: 'Authorize Access' });
  await loginButton.click();

  // Wait for authenticated dashboard view
  await expect(
    page.getByRole('heading', { name: /Gurukul.*Dashboard/i })
  ).toBeVisible({ timeout: 30000 });

  // Save authenticated state
  await page.context().storageState({ path: STORAGE_STATE });
});
