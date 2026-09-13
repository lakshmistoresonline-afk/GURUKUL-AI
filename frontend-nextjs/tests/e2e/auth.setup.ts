import { test as setup, expect } from '@playwright/test';
import { STORAGE_STATE } from '../../playwright.config';

setup('authenticate', async ({ page }) => {
  await page.goto('/');

  const username = process.env.TEST_USERNAME || 'tester_v1';
  const password = process.env.TEST_PASSWORD;

  // Wait for the login form to finish rendering before interacting with it.
  const usernameInput = page.locator('input[type="text"]').first();
  const passwordInput = page.locator('input[type="password"]').first();

  await usernameInput.waitFor({ state: 'visible', timeout: 30000 });
  await passwordInput.waitFor({ state: 'visible', timeout: 30000 });

  await usernameInput.fill(username);
  await passwordInput.fill(password);

  const loginButton = page.getByRole('button', { name: /Authorize Access|Authenticating/i });
  await loginButton.click();

  await page.waitForURL('/', { timeout: 20000 });
  await expect(page.getByText('Unified Dashboard')).toBeVisible();

  await page.context().storageState({ path: STORAGE_STATE });
});
