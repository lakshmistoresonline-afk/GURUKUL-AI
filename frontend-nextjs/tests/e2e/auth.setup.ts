import { test as setup, expect } from '@playwright/test';
import { STORAGE_STATE } from '../../playwright.config';

setup('authenticate', async ({ page }) => {
  await page.goto('/');

  // Check if dashboard is already visible
  const onDashboard = await page.getByText(/Gurukul.*Dashboard/i).isVisible().catch(() => false);
  if (onDashboard) {
    await page.context().storageState({ path: STORAGE_STATE });
    return;
  }

  // Check if login form is present
  const loginHeading = page.getByRole('heading', { name: 'Student Login' });
  if (await loginHeading.isVisible({ timeout: 5000 }).catch(() => false)) {
    const usernameInput = page.locator('input[type="email"], input[type="text"]').first();
    const passwordInput = page.locator('input[type="password"]').first();

    if (await usernameInput.isVisible().catch(() => false)) {
      await usernameInput.fill(process.env.TEST_USERNAME || 'tester_v1@gurukul.ai');
      await passwordInput.fill(process.env.TEST_PASSWORD || 'password123');

      const loginButton = page.getByRole('button', { name: 'Authorize Access' });
      await loginButton.click().catch(() => {});
    }
  }

  // Save authenticated state
  await page.context().storageState({ path: STORAGE_STATE });
});
