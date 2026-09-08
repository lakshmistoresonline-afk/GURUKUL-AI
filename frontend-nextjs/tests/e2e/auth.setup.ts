import { test as setup, expect } from '@playwright/test';
import { STORAGE_STATE } from '../../playwright.config';

setup('authenticate', async ({ page }) => {
  await page.goto('/');

  const username = process.env.TEST_USERNAME || 'tester_v1';
  const password = process.env.TEST_PASSWORD || 'password123';

  await page.fill('input[placeholder="Username"]', username);
  await page.fill('input[placeholder="Password"]', password);
  await page.click('button:has-text("Authorize Access")');

  await page.waitForURL('/', { timeout: 20000 });
  await expect(page.getByText('Student Dashboard')).toBeVisible();

  await page.context().storageState({ path: STORAGE_STATE });
});
